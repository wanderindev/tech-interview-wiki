import json
from typing import Dict, List, Tuple

from anthropic import Anthropic
from flask import current_app

from .constants import (
    RESEARCH_WORD_LIMITS,
    ARTICLE_WORD_LIMITS,
    LEVEL_DESCRIPTIONS,
    RESEARCH_PROMPT_TEMPLATE,
    ARTICLE_GENERATION_PROMPT,
)


class AnthropicClient:
    def __init__(self):
        self.client = Anthropic(api_key=current_app.config["ANTHROPIC_API_KEY"])

    @staticmethod
    def generate_research_prompt(
        title: str, level: str, taxonomy: str, category: str, tags: List[str]
    ) -> str:
        """Generate a research prompt for OpenAI."""
        return RESEARCH_PROMPT_TEMPLATE.format(
            title=title,
            level_description=LEVEL_DESCRIPTIONS[level],
            level=level,
            taxonomy=taxonomy,
            category=category,
            tags=", ".join(tags),
            word_limit=RESEARCH_WORD_LIMITS[level],
        )

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
            parts = content.split("[", 1)
            article_content = parts[0].strip()

            # Parse the JSON array of related articles
            related_articles_json = json.loads("[" + parts[1])

            return article_content, related_articles_json
        except Exception as e:
            current_app.logger.error(f"Error parsing Anthropic response: {e}")
            raise ValueError("Failed to parse Anthropic response") from e
