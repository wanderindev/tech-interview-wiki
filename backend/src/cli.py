import click
from flask.cli import with_appcontext
from services.data_population.populate import DatabasePopulator


@click.command("populate-db")
@click.option("--force", is_flag=True, help="Force regeneration of existing articles")
@with_appcontext
def populate_db_command(force):
    """Populate database with initial articles."""
    populator = DatabasePopulator()
    populator.populate_initial_articles(force=force)
    click.echo("Database population completed.")
