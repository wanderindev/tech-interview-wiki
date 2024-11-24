from typing import List, Tuple

from flask import current_app

from api.articles.models import Article, ArticleLevel
from api.articles.utils import generate_slug
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
            # First, get the existing article
            article = Article.query.filter_by(title=title).first()
            if not article:
                raise ValueError(f"Article with title '{title}' not found in database")

            # Check if we already have research document
            if article.research_result:
                current_app.logger.info(
                    f"Using existing research document for article: {title}"
                )
                research_document = article.research_result
            else:
                current_app.logger.info(
                    f"Generating new research document for article: {title}"
                )
                research_prompt = OpenAIClient.generate_research_prompt(
                    title=title,
                    level=level,
                    taxonomy=taxonomy,
                    category=category,
                    tags=tags,
                )
                research_document = self.openai_client.generate_research(
                    research_prompt
                )

                # Save the research document immediately
                article.research_result = research_document
                db.session.commit()
                current_app.logger.info(f"Saved research document for article: {title}")

            # Generate or update the article content
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
            Article.slug,
            Article.taxonomy,
            Article.category,
            Article.level,
            Article.tags,
        ).all()

        existing_articles_data = [
            {
                "id": art.id,
                "title": art.title,
                "slug": art.slug,
                "taxonomy": art.taxonomy,
                "category": art.category,
                "level": art.level.value,
                "tags": art.tags,
            }
            for art in existing_articles
        ]

        content, related_articles_data = self.anthropic_client.generate_article_content(
            title=title,
            level=level,
            taxonomy=taxonomy,
            category=category,
            tags=tags,
            research_document=research_document,
            existing_articles=existing_articles_data,
        )

        # Update the existing article with generated content
        article = Article.query.filter_by(title=title).first()
        if not article:
            raise ValueError(f"Article with title '{title}' not found in database")

        # Update the article with generated content
        article.content = content
        article.research_result = research_document
        article.is_generated = True

        related_articles = []
        for related_data in related_articles_data:
            if "id" in related_data:  # Reference to existing article
                related_article = Article.query.get(related_data["id"])
            else:  # New article suggestion
                related_article = Article(
                    title=related_data["title"],
                    slug=generate_slug(related_data["title"]),
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
