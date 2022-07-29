import click
import tempfile
import os
from app.services.handlers.generation import generate, validate


DEFAULT_CLUSTERS_PATH_FILE = "CAMINHO-DECK"


def __read_clusters_path():
    path = "."
    CLUSTERS_PATH_FILE = os.path.join(
        os.getenv("APP_BASEDIR"), DEFAULT_CLUSTERS_PATH_FILE
    )
    if os.path.isfile(CLUSTERS_PATH_FILE):
        with open(CLUSTERS_PATH_FILE, "r") as clusterspath:
            path = clusterspath.read().strip()
    return path


@click.group()
def cli():
    """
    Aplicação CLI para geração de decks de NEWAVE com informações
    de clusters de usinas eólicas.
    """
    pass


@click.command("validaarquivos")
@click.option(
    "--clusters",
    default=None,
    help="diretório com os arquivos resultantes da clusterização",
)
@click.argument(
    "deck",
)
def validatefiles(clusters, deck):
    """
    Valida o deck para o processamento. Confere se os arquivos necessários
    estão no ZIP e se contém as informações necessárias no processamento.

    DECK: arquivos de entrada do NEWAVE comprimidos em um .zip
    """
    if clusters is None:
        clusters = __read_clusters_path()
    os.environ["CLUSTERSDIR"] = clusters
    os.environ["DECK"] = deck
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.environ["TMPDIR"] = tmpdirname
        validate()


@click.command("geradeck")
@click.option(
    "--clusters",
    default=None,
    help="diretório com os arquivos resultantes da clusterização",
)
@click.argument(
    "deck",
)
def generatedeck(clusters, deck):
    """
    Processa o deck, realiza as alterações necessárias e gera os arquivos
    novos para consideração da geração eólica.

    DECK: arquivos de entrada do NEWAVE comprimidos em um .zip
    """
    if clusters is None:
        clusters = __read_clusters_path()
    os.environ["CLUSTERSDIR"] = clusters
    os.environ["DECK"] = deck
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.environ["TMPDIR"] = tmpdirname
        generate()


cli.add_command(validatefiles)
cli.add_command(generatedeck)
