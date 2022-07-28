import click
import tempfile
import os
from app.services.handlers.generation import generate, validate
from app.models.settings import Settings
from app.utils.log import Log

DEFAULT_DECK_NAME = "deck.zip"
DEFAULT_CLUSTERS_DIR = "/tmp/eolicas-newave-app/results"


@click.group()
def cli():
    pass


@click.command("validaarquivos")
@click.option(
    "--clusters",
    default=DEFAULT_CLUSTERS_DIR,
    help="diretório com os arquivos resultantes da clusterização",
)
@click.option(
    "--deck",
    default=DEFAULT_DECK_NAME,
    help="arquivos de entrada do NEWAVE comprimidos em um .zip",
)
def validatefiles(clusters, deck):
    os.environ["CLUSTERSDIR"] = clusters
    os.environ["DECK"] = deck
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.environ["TMPDIR"] = tmpdirname
        validate()


@click.command("geradeck")
@click.option(
    "--clusters",
    default=DEFAULT_CLUSTERS_DIR,
    help="diretório com os arquivos resultantes da clusterização",
)
@click.option(
    "--deck",
    default=DEFAULT_DECK_NAME,
    help="arquivos de entrada do NEWAVE comprimidos em um .zip",
)
def generatedeck(clusters, deck):
    os.environ["CLUSTERSDIR"] = clusters
    os.environ["DECK"] = deck
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.environ["TMPDIR"] = tmpdirname
        generate()


cli.add_command(validatefiles)
cli.add_command(generatedeck)
