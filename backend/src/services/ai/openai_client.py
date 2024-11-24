from typing import List

import openai
from flask import current_app

from .constants import (
    RESEARCH_WORD_LIMITS,
    LEVEL_DESCRIPTIONS,
    RESEARCH_PROMPT_TEMPLATE,
)


class OpenAIClient:
    def __init__(self):
        self.client = openai.OpenAI(api_key=current_app.config["OPENAI_API_KEY"])

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

    def generate_research(self, prompt: str) -> str:
        """Generate research document using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model="o1-preview",
                messages=[
                    {
                        "role": "assistant",
                        "content": "You are a technical writer researching content for programming interview preparation articles.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )

            return response.choices[0].message.content

        except Exception as e:
            current_app.logger.error(f"Error generating research with OpenAI: {e}")
            raise ValueError("Failed to generate research document") from e
