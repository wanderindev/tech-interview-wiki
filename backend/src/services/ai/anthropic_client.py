import json
import time
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
    ) -> Tuple[str, str, List[Dict]]:
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

        # Add a small delay before making the request
        time.sleep(0.1)

        response = self.client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=4096,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}],
        )

        # Ensure we have a complete response
        content = response.content[0].text
        if not content:
            raise ValueError("Empty response from Anthropic API")

        # Add a small delay after getting the response
        time.sleep(0.1)

        # Basic validation before parsing
        if not all(
            marker in content
            for marker in [
                "EXCERPT_START",
                "EXCERPT_END",
                "RELATED_ARTICLES_START",
                "RELATED_ARTICLES_END",
            ]
        ):
            raise ValueError("Response missing required markers")

        # Parse the response with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                (
                    excerpt,
                    article_content,
                    related_articles_json,
                ) = AnthropicClient._parse_response(content)
                return excerpt, article_content, related_articles_json
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(0.2 * (attempt + 1))

    @staticmethod
    def _parse_response(content: str) -> Tuple[str, str, List[Dict]]:
        """Parse the response to separate excerpt, article content, and related articles."""
        try:
            # Debug position of markers
            current_app.logger.debug(f"Content length: {len(content)}")
            current_app.logger.debug(f"First 100 chars: {content[:100]}")
            current_app.logger.debug(f"Last 100 chars: {content[-100:]}")

            # Extract excerpt
            excerpt_start = content.find("EXCERPT_START")
            excerpt_end = content.find("EXCERPT_END")

            current_app.logger.debug(
                f"Excerpt markers: start={excerpt_start}, end={excerpt_end}"
            )

            if excerpt_start == -1 or excerpt_end == -1:
                current_app.logger.error("Missing excerpt markers")
                raise ValueError("Response does not contain proper excerpt markers")

            excerpt = content[
                excerpt_start + len("EXCERPT_START") : excerpt_end
            ].strip()
            current_app.logger.debug(f"Extracted excerpt: {excerpt[:50]}...")

            # Look for related articles section
            start_marker = "RELATED_ARTICLES_START"
            end_marker = "RELATED_ARTICLES_END"

            json_start = content.find(start_marker)
            json_end = content.find(end_marker)

            current_app.logger.debug(
                f"JSON markers: start={json_start}, end={json_end}"
            )

            if json_start == -1:
                current_app.logger.error("No 'RELATED_ARTICLES_START' marker found")
                raise ValueError("Response does not contain related articles section")

            if json_end == -1:
                current_app.logger.error("No 'RELATED_ARTICLES_END' marker found")
                raise ValueError("Response does not contain end marker")

            # Extract article content
            article_content_start = excerpt_end + len("EXCERPT_END")
            article_content = content[article_content_start:json_start].strip()

            # Debug content lengths
            current_app.logger.debug(f"Article content length: {len(article_content)}")
            current_app.logger.debug(
                f"Article content starts with: {article_content[:50]}..."
            )

            # Extract and parse JSON content
            json_content = content[json_start + len(start_marker) : json_end].strip()
            current_app.logger.debug(f"JSON content length: {len(json_content)}")
            current_app.logger.debug(
                f"JSON content starts with: {json_content[:50]}..."
            )

            try:
                data = json.loads(json_content)
                current_app.logger.debug(
                    f"Successfully parsed JSON with keys: {data.keys()}"
                )

                if not isinstance(data, dict) or "articles" not in data:
                    current_app.logger.error(
                        f"Invalid JSON structure. Data type: {type(data)}"
                    )
                    raise ValueError("Invalid JSON structure: missing articles array")

                related_articles = data["articles"]
                current_app.logger.debug(
                    f"Found {len(related_articles)} related articles"
                )

                return excerpt, article_content, related_articles

            except json.JSONDecodeError as e:
                current_app.logger.error(f"JSON parsing error: {e}")
                current_app.logger.error(f"Attempted to parse:\n{json_content}")
                raise ValueError(f"Failed to parse JSON: {e}")

        except Exception as e:
            current_app.logger.error(f"Error parsing Anthropic response: {e}")
            current_app.logger.error(f"Full response content:\n{content}")
            raise ValueError("Failed to parse Anthropic response") from e
