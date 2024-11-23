from typing import List, Tuple

from flask import current_app

from api.articles.models import Article, ArticleLevel
from extensions import db
from .anthropic_client import AnthropicClient
from .openai_client import OpenAIClient


class ArticleGenerator:
    def __init__(self):
        self.anthropic_client = AnthropicClient()
        self.openai_client = OpenAIClient()

    def research_and_generate_article(
        self, title: str, level: str, taxonomy: str, category: str, tags: List[str]
    ) -> Tuple[Article, List[Article]]:
        """Complete workflow to research and generate an article."""
        try:
            research_prompt = OpenAIClient.generate_research_prompt(
                title=title,
                level=level,
                taxonomy=taxonomy,
                category=category,
                tags=tags,
            )
            research_document = self.openai_client.generate_research(research_prompt)

            return self.generate_article(
                title=title,
                level=level,
                taxonomy=taxonomy,
                category=category,
                tags=tags,
                research_document=research_document,
            )

        except Exception as e:
            current_app.logger.error(f"Error in research_and_generate_article: {e}")
            raise

    def generate_article(
        self,
        title: str,
        level: str,
        taxonomy: str,
        category: str,
        tags: List[str],
        research_document: str,
    ) -> Tuple[Article, List[Article]]:
        """Generate article content and create related article records."""
        existing_articles = Article.query.with_entities(
            Article.id,
            Article.title,
            Article.taxonomy,
            Article.category,
            Article.level,
            Article.tags,
        ).all()

        # noinspection PyProtectedMember
        content, related_articles_data = self.anthropic_client.generate_article_content(
            title=title,
            level=level,
            taxonomy=taxonomy,
            category=category,
            tags=tags,
            research_document=research_document,
            existing_articles=[art._asdict() for art in existing_articles],
        )

        article = Article(
            title=title,
            level=ArticleLevel[level.upper()],
            taxonomy=taxonomy,
            category=category,
            tags=tags,
            content=content,
            research_result=research_document,
            is_generated=True,
        )
        db.session.add(article)

        related_articles = []
        for related_data in related_articles_data:
            if "id" in related_data:  # Reference to existing article
                related_article = Article.query.get(related_data["id"])
            else:  # New article suggestion
                related_article = Article(
                    title=related_data["title"],
                    slug=related_data["slug"],
                    level=ArticleLevel[related_data["level"].upper()],
                    taxonomy=related_data["taxonomy"],
                    category=related_data["category"],
                    tags=related_data["tags"],
                    is_generated=False,
                )
                db.session.add(related_article)

            related_articles.append(related_article)

        article.related_articles = related_articles
        db.session.commit()

        return article, related_articles
