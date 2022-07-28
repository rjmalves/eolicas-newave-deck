import logging
import logging.handlers
from os.path import join

from app.utils.singleton import Singleton


class Log(metaclass=Singleton):

    FILE = "eolicas-newave-deck.log"
    LOGGER = None

    @classmethod
    def configure_logging(cls, directory: str):
        root = logging.getLogger("main")
        h = logging.handlers.RotatingFileHandler(
            join(directory, cls.FILE), "a", 10000, 0, "utf-8"
        )
        f = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
        h.setFormatter(f)
        # Logger para STDOUT
        std_h = logging.StreamHandler()
        std_h.setFormatter(f)
        root.addHandler(h)
        root.addHandler(std_h)
        root.setLevel(logging.INFO)
        cls.LOGGER = root

    @classmethod
    def log(cls) -> logging.Logger:
        if cls.LOGGER is None:
            raise ValueError("Logger não configurado!")
        return cls.LOGGER
