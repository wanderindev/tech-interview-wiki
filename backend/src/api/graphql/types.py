from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import strawberry

from api.articles.models import Article


class Level(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


ArticleLevelEnum = strawberry.enum(Level)


@dataclass
@strawberry.type
class ArticleType:
    id: int
    title: str
    slug: str
    level: str
    taxonomy: str
    category: str
    tags: List[str]
    content: Optional[str]
    excerpt: Optional[str]  # Make sure we include excerpt
    is_generated: bool
    word_count: int
    updated_at: Optional[str]
    related_articles: List["ArticleType"]  # Add related articles

    @classmethod
    def from_orm(cls, article: Article) -> "ArticleType":
        return cls(
            id=article.id,
            title=article.title,
            slug=article.slug,
            level=article.level.value,
            taxonomy=article.taxonomy,
            category=article.category,
            tags=article.tags,
            content=article.content,
            excerpt=article.excerpt,
            is_generated=article.is_generated,
            word_count=article.word_count,
            updated_at=article.updated_at.isoformat() if article.updated_at else None,
            related_articles=[
                ArticleType.from_orm(related) for related in article.related_articles
            ]
            if article.related_articles
            else [],
        )


@dataclass
@strawberry.type
class TaxonomyStats:
    taxonomy: str
    total_articles: int
    categories: List[str]


@dataclass
@strawberry.type
class CategoryStats:
    category: str
    taxonomy: str
    total_articles: int
    levels: List[str]
