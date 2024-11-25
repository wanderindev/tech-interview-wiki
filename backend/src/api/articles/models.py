import enum
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ARRAY

from extensions import db


class ArticleLevel(enum.Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    level = db.Column(db.Enum(ArticleLevel), nullable=False)

    # Categorization
    taxonomy = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    tags = db.Column(ARRAY(db.String(50)), nullable=False, default=list)

    # Content
    content = db.Column(db.Text, nullable=True)
    excerpt = db.Column(db.Text, nullable=True)
    word_count = db.Column(db.Integer, nullable=False, default=0)
    relevance_score = db.Column(db.Float, nullable=False, default=0.0)

    # AI Generation Fields
    research_result = db.Column(db.Text, nullable=True)

    # Status tracking
    is_generated = db.Column(db.Boolean, default=False, nullable=False)
    generation_started_at = db.Column(db.DateTime, nullable=True)
    last_generation_error = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    related_articles = db.relationship(
        "Article",
        secondary="article_relationships",
        primaryjoin="Article.id == article_relationships.c.article_id",
        secondaryjoin="Article.id == article_relationships.c.related_article_id",
        backref="referenced_by",
    )

    @property
    def needs_generation(self) -> bool:
        """Check if article content needs to be generated."""
        return not self.content or not self.is_generated

    def mark_generation_started(self) -> None:
        """Mark that content generation has started."""
        self.generation_started_at = datetime.now(timezone.utc)
        self.last_generation_error = None
        db.session.commit()

    def mark_generation_complete(self) -> None:
        """Mark that content generation is complete."""
        self.is_generated = True
        self.generation_started_at = None
        self.last_generation_error = None
        db.session.commit()

    def mark_generation_failed(self, error: str) -> None:
        """Mark that content generation failed."""
        self.is_generated = False
        self.generation_started_at = None
        self.last_generation_error = error
        db.session.commit()

    @classmethod
    def create_from_suggestion(cls, data: dict) -> "Article":
        """Create a new article from an AI suggestion."""
        article = cls(
            title=data["title"],
            slug=data["slug"],
            level=data["level"],
            taxonomy=data["taxonomy"],
            category=data["category"],
            tags=data["tags"],
            is_generated=False,
        )
        db.session.add(article)
        db.session.commit()
        return article

    def update_word_count(self):
        if self.content:
            self.word_count = len(self.content.split())
        else:
            self.word_count = 0

    def calculate_relevance_score(self):
        score = 0.0

        # Taxonomy relevance (articles in taxonomy)
        taxonomy_count = (
            db.session.query(func.count(Article.id))
            .filter(Article.taxonomy == self.taxonomy)
            .scalar()
        )
        score += taxonomy_count * (2.0 if self.is_generated else 0.5)

        # Link backs (appearances in related articles)
        linkback_count = (
            db.session.query(func.count())
            .select_from(article_relationships)
            .filter(article_relationships.c.related_article_id == self.id)
            .scalar()
        )
        score += linkback_count

        # Generation status
        score += 1.0 if self.is_generated else 0.0

        # Tags count
        score += len(self.tags)

        # Level score
        level_scores = {
            ArticleLevel.BASIC: 0.0,
            ArticleLevel.INTERMEDIATE: 2.0,
            ArticleLevel.ADVANCED: 1.0,
        }
        score += level_scores[self.level]

        return score

    def update_relevance_score(self):
        """Update the relevance score and save to database"""
        self.relevance_score = self.calculate_relevance_score()
        db.session.commit()


article_relationships = db.Table(
    "article_relationships",
    db.Column("article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True),
    db.Column(
        "related_article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True
    ),
)
