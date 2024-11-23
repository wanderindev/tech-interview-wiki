import enum
from datetime import datetime, timezone

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


article_relationships = db.Table(
    "article_relationships",
    db.Column("article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True),
    db.Column(
        "related_article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True
    ),
)
