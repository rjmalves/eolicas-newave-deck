import click
import tempfile
import os


DEFAULT_DECK_NAME = "deck.zip"
DEFAULT_CLUSTERS_DIR = "/tmp/eolicas-newave-app/results"


@click.group()
def cli():
    pass


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
def generate(clustersdir, deck):
    os.environ["CLUSTERSDIR"] = clustersdir
    os.environ["DECK"] = deck
    click.echo("Gerando deck de eólica para o NEWAVE...")
    click.echo(f"Deck: {deck}")
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.environ["TMPDIR"] = tmpdirname
        click.echo(f"Criado diretório temporário: {tmpdirname}")


cli.add_command(generate)
