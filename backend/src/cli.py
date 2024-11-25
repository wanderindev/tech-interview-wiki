import click
from flask.cli import with_appcontext
from api.articles.models import Article
from extensions import db
from services.data_population.populate import DatabasePopulator


@click.command("populate-db")
@click.option("--force", is_flag=True, help="Force regeneration of existing articles")
@with_appcontext
def populate_db_command(force):
    """Populate database with initial articles."""
    populator = DatabasePopulator()
    populator.populate_initial_articles(force=force)
    click.echo("Database population completed.")


@click.command("update-word-counts")
@with_appcontext
def update_word_counts_command():
    """Update word_count for all articles with content."""
    try:
        # Get all articles with content
        articles = Article.query.filter(Article.content.isnot(None)).all()

        if not articles:
            click.echo("No articles with content found.")
            return

        updated_count = 0
        for article in articles:
            # Count words in content (splitting by whitespace)
            word_count = len(article.content.split())
            article.word_count = word_count
            updated_count += 1

        db.session.commit()
        click.echo(f"Successfully updated word count for {updated_count} articles.")

    except Exception as e:
        db.session.rollback()
        click.echo(f"Error updating word counts: {str(e)}", err=True)
        raise


@click.command("update-relevance-scores")
@with_appcontext
def update_relevance_scores_command():
    """Update relevance scores for all articles."""
    articles = Article.query.all()
    for article in articles:
        article.update_relevance_score()
    click.echo("Updated relevance scores for all articles.")
