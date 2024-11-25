import json
from typing import Dict, List, Tuple

from anthropic import Anthropic
from flask import current_app

from .constants import (
    ARTICLE_WORD_LIMITS,
    LEVEL_DESCRIPTIONS,
    ARTICLE_GENERATION_PROMPT,
)


class AnthropicClient:
    def __init__(self):
        self.client = Anthropic(api_key=current_app.config["ANTHROPIC_API_KEY"])

    def generate_article_content(
        self,
        title: str,
        level: str,
        taxonomy: str,
        category: str,
        tags: List[str],
        research_document: str,
        existing_articles: List[Dict],
    ) -> Tuple[str, List[Dict]]:
        """Generate article content and related articles."""

        # Format existing articles for the prompt
        existing_articles_text = json.dumps(
            [
                {
                    "id": art["id"],
                    "title": art["title"],
                    "taxonomy": art["taxonomy"],
                    "category": art["category"],
                    "level": art["level"],
                    "tags": art["tags"],
                }
                for art in existing_articles
            ],
            indent=2,
        )

        prompt = ARTICLE_GENERATION_PROMPT.format(
            title=title,
            level_description=LEVEL_DESCRIPTIONS[level],
            taxonomy=taxonomy,
            category=category,
            tags=", ".join(tags),
            word_limit=ARTICLE_WORD_LIMITS[level],
            existing_articles=existing_articles_text,
            research_document=research_document,
        )

        # noinspection PyUnresolvedReferences
        response = self.client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=4096,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.content[0].text

        # Split content into article and related articles
        (
            excerpt,
            article_content,
            related_articles_json,
        ) = AnthropicClient._parse_response(content)

        return excerpt, article_content, related_articles_json

    @staticmethod
    def _parse_response(content: str) -> Tuple[str, str, List[Dict]]:
        """
        Parse the response to separate excerpt, article content, and related articles.

        Returns:
            Tuple containing (excerpt, article_content, related_articles)
        """
        try:
            # Extract excerpt
            excerpt_start = content.find("EXCERPT_START")
            excerpt_end = content.find("EXCERPT_END")

            if excerpt_start == -1 or excerpt_end == -1:
                current_app.logger.error("Missing excerpt markers")
                raise ValueError("Response does not contain proper excerpt markers")

            excerpt = content[
                excerpt_start + len("EXCERPT_START") : excerpt_end
            ].strip()

            # Look for the related articles section
            start_marker = "RELATED_ARTICLES_START"
            end_marker = "RELATED_ARTICLES_END"

            json_start = content.find(start_marker)
            json_end = content.find(end_marker)

            if json_start == -1:
                current_app.logger.error("No 'RELATED_ARTICLES_START' marker found")
                raise ValueError("Response does not contain related articles section")

            if json_end == -1:
                current_app.logger.error("No 'RELATED_ARTICLES_END' marker found")
                raise ValueError("Response does not contain end marker")

            # Extract the article content (everything between excerpt and related articles)
            article_content = content[
                excerpt_end + len("EXCERPT_END") : json_start
            ].strip()

            # Extract and parse the JSON content
            json_content = content[json_start + len(start_marker) : json_end].strip()

            try:
                data = json.loads(json_content)

                # Validate the structure
                if not isinstance(data, dict):
                    raise ValueError("Parsed JSON is not an object")

                if "articles" not in data or "existing_articles_map" not in data:
                    raise ValueError(
                        "JSON missing required fields: articles and existing_articles_map"
                    )

                related_articles = data["articles"]
                existing_map = data["existing_articles_map"]

                if not isinstance(related_articles, list):
                    raise ValueError("articles field is not a list")

                if len(related_articles) != 5:
                    raise ValueError(
                        f"Expected 5 related articles, got {len(related_articles)}"
                    )

                # Validate each article
                for idx, article in enumerate(related_articles):
                    # If this article is in the existing_map, replace it with a reference
                    str_idx = str(idx)
                    if str_idx in existing_map:
                        related_articles[idx] = {"id": existing_map[str_idx]}
                    else:
                        required_fields = {
                            "title",
                            "taxonomy",
                            "category",
                            "level",
                            "tags",
                            "excerpt",
                        }
                        if not all(field in article for field in required_fields):
                            raise ValueError(
                                f"Article missing required fields: {required_fields - set(article.keys())}"
                            )

                        if article["level"] not in [
                            "basic",
                            "intermediate",
                            "advanced",
                        ]:
                            raise ValueError(f"Invalid level value: {article['level']}")

                        # Validate excerpt length (approximately 80 words)
                        if len(article["excerpt"].split()) > 90:  # Give some margin
                            current_app.logger.warning(
                                f"Related article excerpt too long: {len(article['excerpt'].split())} words"
                            )

                # Validate main excerpt length (approximately 80 words)
                if len(excerpt.split()) > 90:  # Give some margin
                    current_app.logger.warning(
                        f"Main excerpt too long: {len(excerpt.split())} words"
                    )

                return excerpt, article_content, related_articles

            except json.JSONDecodeError as e:
                current_app.logger.error(f"JSON parsing error: {e}")
                current_app.logger.error(f"Attempted to parse: {json_content}")
                raise ValueError(f"Failed to parse JSON: {e}")

        except Exception as e:
            current_app.logger.error(f"Error parsing Anthropic response: {e}")
            current_app.logger.error(f"Full response content: {content}")
            raise ValueError("Failed to parse Anthropic response") from e
