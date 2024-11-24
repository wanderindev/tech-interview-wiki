import logging
import time

from api.articles.models import Article, ArticleLevel
from extensions import db
from services.ai.article_generator import ArticleGenerator
from .initial_articles import INITIAL_ARTICLES

logger = logging.getLogger(__name__)


class DatabasePopulator:
    def __init__(self):
        self.article_generator = ArticleGenerator()

    def populate_initial_articles(self, force: bool = False) -> None:
        """
        Populate the database with initial articles metadata and then generate content.

        Args:
            force: If True, will generate content even for existing articles
        """
        try:
            if not force and Article.query.count() > 0:
                logger.info("Database already contains articles. Skipping population.")
                return

            logger.info("Starting database population with initial articles...")

            # Phase 1: Create article metadata
            DatabasePopulator._create_article_metadata()

            # Phase 2: Generate content for articles
            self._generate_article_content()

            logger.info("Database population completed successfully.")

        except Exception as e:
            logger.error(f"Error during database population: {str(e)}")
            raise

    @staticmethod
    def _create_article_metadata() -> None:
        """Create initial article records with metadata only."""
        logger.info("Phase 1: Creating article metadata...")

        for article_data in INITIAL_ARTICLES:
            try:
                # Check if article already exists
                existing_article = Article.query.filter_by(
                    title=article_data["title"]
                ).first()

                if existing_article:
                    logger.info(
                        f"Article metadata '{article_data['title']}' already exists."
                    )
                    continue

                # Create new article with metadata only
                article = Article(
                    title=article_data["title"],
                    taxonomy=article_data["taxonomy"],
                    category=article_data["category"],
                    level=ArticleLevel[article_data["level"].upper()],
                    tags=article_data["tags"],
                    is_generated=False,
                )

                db.session.add(article)
                logger.info(f"Created metadata for article: {article_data['title']}")

            except Exception as e:
                logger.error(
                    f"Error creating metadata for article '{article_data['title']}': {str(e)}"
                )
                db.session.rollback()
                continue

        try:
            db.session.commit()
            logger.info("Successfully created all article metadata.")
        except Exception as e:
            logger.error(f"Error committing article metadata: {str(e)}")
            db.session.rollback()
            raise

    def _generate_article_content(self) -> None:
        """Generate content for articles that don't have it yet."""
        logger.info("Phase 2: Generating article content...")

        # Get all articles that need content generation
        articles_to_generate = Article.query.filter_by(is_generated=False).all()

        for article in articles_to_generate:
            try:
                logger.info(f"Generating content for article: {article.title}")

                (
                    article,
                    related_articles,
                ) = self.article_generator.research_and_generate_article(
                    title=article.title,
                    level=article.level.value,
                    taxonomy=article.taxonomy,
                    category=article.category,
                    tags=article.tags,
                )

                logger.info(
                    f"Successfully generated article '{article.title}' "
                    f"with {len(related_articles)} related articles"
                )

                # Sleep to respect API rate limits
                time.sleep(2)

            except Exception as e:
                logger.error(
                    f"Error generating content for article '{article.title}': {str(e)}"
                )
                continue

        logger.info("Completed content generation phase.")
