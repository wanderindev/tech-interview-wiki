from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Tuple

from flask import current_app

from api.articles.models import Article, ArticleLevel
from api.articles.utils import generate_slug
from extensions import db
from .anthropic_client import AnthropicClient
from .openai_client import OpenAIClient


class ArticleMatcher:
    TITLE_SIMILARITY_THRESHOLD = 0.85

    @staticmethod
    def compute_similarity(str1: str, str2: str) -> float:
        """Compute string similarity ratio."""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    @staticmethod
    def find_similar_article(
        new_article: Dict[str, Any], existing_articles: List[Dict[str, Any]]
    ) -> Optional[int]:
        """Find if a similar article exists in the database."""
        for existing in existing_articles:
            # Check exact title match
            if new_article["title"].lower() == existing["title"].lower():
                return existing["id"]

            # Check title similarity
            if (
                ArticleMatcher.compute_similarity(
                    new_article["title"], existing["title"]
                )
                > ArticleMatcher.TITLE_SIMILARITY_THRESHOLD
            ):
                # Additional validation: check category and taxonomy match
                if (
                    new_article["category"] == existing["category"]
                    and new_article["taxonomy"] == existing["taxonomy"]
                ):
                    return existing["id"]

            # Check tag overlap
            common_tags = set(new_article["tags"]) & set(existing["tags"])
            if len(common_tags) >= 3:  # If 3 or more tags match
                if (
                    ArticleMatcher.compute_similarity(
                        new_article["title"], existing["title"]
                    )
                    > 0.7
                ):  # Lower threshold if tags match
                    return existing["id"]

        return None


class ArticleGenerator:
    def __init__(self):
        self.anthropic_client = AnthropicClient()
        self.openai_client = OpenAIClient()

    def research_and_generate_article(
        self,
        title: str,
        level: str,
        taxonomy: str,
        category: str,
        tags: List[str],
        excerpt: str,
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
                    excerpt=excerpt,
                )
                research_document = self.openai_client.generate_research(
                    research_prompt
                )

                # Save the research document immediately
                article.research_result = research_document
                db.session.commit()
                current_app.logger.info(f"Saved research document for article: {title}")

            # Generate or update the article content
            try:
                return self.generate_article(
                    title=title,
                    level=level,
                    taxonomy=taxonomy,
                    category=category,
                    tags=tags,
                    research_document=research_document,
                )
            except Exception as article_error:
                current_app.logger.error(
                    f"Error in generate_article: {str(article_error)}"
                )
                current_app.logger.error(
                    f"Research document: {research_document[:200]}..."
                )
                raise

        except Exception as e:
            current_app.logger.error(
                f"Error in research_and_generate_article: {str(e)}"
            )
            current_app.logger.error(f"Full error type: {type(e)}")
            current_app.logger.error(f"Error args: {e.args}")
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
        # Get existing articles for context
        existing_articles = Article.query.with_entities(
            Article.id,
            Article.title,
            Article.taxonomy,
            Article.category,
            Article.level,
            Article.tags,
        ).all()

        # Convert to dictionary and handle enum serialization
        existing_articles_data = [
            {
                "id": art.id,
                "title": art.title,
                "taxonomy": art.taxonomy,
                "category": art.category,
                "level": art.level.value,
                "tags": art.tags,
            }
            for art in existing_articles
        ]

        # Generate content using Anthropic
        (
            excerpt,
            content,
            related_articles_data,
        ) = self.anthropic_client.generate_article_content(
            title=title,
            level=level,
            taxonomy=taxonomy,
            category=category,
            tags=tags,
            research_document=research_document,
            existing_articles=existing_articles_data,
        )

        # Process related articles with similarity checking
        related_articles = []
        for article_data in related_articles_data:
            if "id" in article_data:
                # Direct reference to existing article
                related_article = Article.query.get(article_data["id"])
            else:
                # Check for similar existing articles
                similar_id = ArticleMatcher.find_similar_article(
                    article_data, existing_articles_data
                )

                if similar_id:
                    related_article = Article.query.get(similar_id)
                    current_app.logger.info(
                        f"Found similar existing article: {related_article.title}"
                    )
                else:
                    # Create new article
                    related_article = Article(
                        title=article_data["title"],
                        slug=generate_slug(article_data["title"]),
                        level=ArticleLevel[article_data["level"].upper()],
                        taxonomy=article_data["taxonomy"],
                        category=article_data["category"],
                        tags=article_data["tags"],
                        is_generated=False,
                        excerpt=article_data["excerpt"],
                    )
                    db.session.add(related_article)

            related_articles.append(related_article)

        # Update the existing article
        article = Article.query.filter_by(title=title).first()
        article.content = content
        article.excerpt = excerpt
        article.research_result = research_document
        article.is_generated = True
        article.related_articles = related_articles

        db.session.commit()

        return article, related_articles
