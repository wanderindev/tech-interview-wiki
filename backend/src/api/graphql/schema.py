from threading import Thread
from typing import List, Optional

import strawberry
from flask import current_app
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from api.articles.models import Article
from services.ai.article_generator import ArticleGenerator
from .types import ArticleType, TaxonomyStats, CategoryStats, ArticleLevelEnum


@strawberry.type
class Query:
    @strawberry.field(description="Get an article by its slug")
    def article_by_slug(self, slug: str) -> Optional[ArticleType]:
        article = Query.resolve_article_by_slug(slug)

        if article and not article.is_generated:
            article_generator = ArticleGenerator()
            app = current_app._get_current_object()

            def generate_with_context():
                with app.app_context():
                    article_generator.research_and_generate_article(
                        article.title,
                        article.level.value,
                        article.taxonomy,
                        article.category,
                        article.tags,
                        article.excerpt,
                    )

            thread = Thread(target=generate_with_context)
            thread.daemon = True
            thread.start()

        return article

    @staticmethod
    def resolve_article_by_slug(slug: str) -> Optional[Article]:
        return (
            Article.query.options(joinedload(Article.related_articles))
            .filter_by(slug=slug)
            .first()
        )

    @strawberry.field(description="Get all articles")
    def all_articles(self) -> List[ArticleType]:
        return Query.resolve_all_articles()

    @staticmethod
    def resolve_all_articles() -> List[Article]:
        return Article.query.order_by(Article.relevance_score.desc()).all()

    @strawberry.field(description="Get articles by taxonomy")
    def articles_by_taxonomy(self, taxonomy: str) -> List[ArticleType]:
        return Query.resolve_articles_by_taxonomy(taxonomy)

    @staticmethod
    def resolve_articles_by_taxonomy(taxonomy: str) -> List[ArticleType]:
        articles = Article.query.filter_by(taxonomy=taxonomy).all()
        return [ArticleType.from_orm(article) for article in articles]

    @strawberry.field(description="Get articles by category and optional taxonomy")
    def articles_by_category(
        self, category: str, taxonomy: Optional[str] = None
    ) -> List[ArticleType]:
        return Query.resolve_articles_by_category(category, taxonomy)

    @staticmethod
    def resolve_articles_by_category(
        category: str, taxonomy: Optional[str] = None
    ) -> List[ArticleType]:
        query = Article.query.filter_by(category=category)
        if taxonomy:
            query = query.filter_by(taxonomy=taxonomy)
        return [ArticleType.from_orm(article) for article in query.all()]

    @strawberry.field(description="Get articles by difficulty level")
    def articles_by_level(self, level: ArticleLevelEnum) -> List[ArticleType]:
        return Query.resolve_articles_by_level(level)

    @staticmethod
    def resolve_articles_by_level(level: ArticleLevelEnum) -> List[ArticleType]:
        articles = Article.query.filter_by(level=level.value).all()
        return [ArticleType.from_orm(article) for article in articles]

    @strawberry.field(description="Get statistics about all taxonomies")
    def all_taxonomies(self) -> List[TaxonomyStats]:
        return Query.resolve_all_taxonomies()

    @staticmethod
    def resolve_all_taxonomies() -> List[TaxonomyStats]:
        results = (
            db.session.query(
                Article.taxonomy,
                func.count(Article.id).label("total"),
                func.array_agg(func.distinct(Article.category)).label("categories"),
            )
            .group_by(Article.taxonomy)
            .all()
        )

        return [
            TaxonomyStats(taxonomy=r[0], total_articles=r[1], categories=r[2])
            for r in results
        ]

    @strawberry.field(description="Get statistics about all categories")
    def all_categories(self) -> List[CategoryStats]:
        return Query.resolve_all_categories()

    @staticmethod
    def resolve_all_categories() -> List[CategoryStats]:
        results = (
            db.session.query(
                Article.category,
                Article.taxonomy,
                func.count(Article.id).label("total"),
                func.array_agg(func.distinct(Article.level)).label("levels"),
            )
            .group_by(Article.category, Article.taxonomy)
            .all()
        )

        return [
            CategoryStats(
                category=r[0],
                taxonomy=r[1],
                total_articles=r[2],
                levels=[level.value for level in r[3]],
            )
            for r in results
        ]


schema = strawberry.Schema(query=Query)
