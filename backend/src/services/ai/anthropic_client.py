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
        article_content, related_articles_json = AnthropicClient._parse_response(
            content
        )

        return article_content, related_articles_json

    @staticmethod
    def _parse_response(content: str) -> Tuple[str, List[Dict]]:
        """Parse the response to separate article content from related articles."""
        try:
            # Look for the Suggested Related Articles section
            marker = "Suggested Related Articles:"
            json_start = content.find(marker)

            if json_start == -1:
                current_app.logger.error(
                    "No 'Suggested Related Articles:' section found"
                )
                raise ValueError("Response does not contain related articles section")

            # Find the JSON array after the marker
            json_content = content[json_start + len(marker) :].strip()

            # If the JSON is wrapped in ```json ```, remove it
            if json_content.startswith("```json"):
                json_content = json_content[7:].strip()  # Remove ```json
                json_content = json_content.rstrip("`")  # Remove trailing backticks

            # Get everything before the JSON as article content
            article_content = content[:json_start].strip()

            # Parse the JSON array
            try:
                related_articles_json = json.loads(json_content)

                # Validate the structure
                if not isinstance(related_articles_json, list):
                    raise ValueError("Parsed JSON is not a list")

                for article in related_articles_json:
                    required_fields = {"title", "taxonomy", "category", "level", "tags"}
                    if not all(field in article for field in required_fields):
                        raise ValueError(
                            f"Article missing required fields: {required_fields - set(article.keys())}"
                        )

            except json.JSONDecodeError as e:
                current_app.logger.error(f"JSON parsing error: {e}")
                current_app.logger.error(f"Attempted to parse: {json_content}")
                raise ValueError(f"Failed to parse JSON: {e}")

            return article_content, related_articles_json

        except Exception as e:
            current_app.logger.error(f"Error parsing Anthropic response: {e}")
            current_app.logger.error(f"Full response content: {content}")
            raise ValueError("Failed to parse Anthropic response") from e
