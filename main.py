from app.app import cli
from dotenv import load_dotenv
import os
import pathlib

BASEDIR = pathlib.Path().resolve()
os.environ["APP_INSTALLDIR"] = os.path.dirname(os.path.abspath(__file__))
load_dotenv(
    pathlib.Path(os.getenv("APP_INSTALLDIR")).joinpath(
        "eolicas-newave-deck.cfg"
    ),
    override=True,
)
os.environ["APP_BASEDIR"] = str(BASEDIR)
load_dotenv(BASEDIR.joinpath("eolicas-newave-deck.cfg"), override=True)

if __name__ == "__main__":
    cli()
