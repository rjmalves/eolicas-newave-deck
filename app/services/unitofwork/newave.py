from abc import ABC, abstractmethod
from os import chdir, curdir
import re
from typing import Dict
from pathlib import Path


from app.adapters.repository.newave import (
    AbstractNewaveRepository,
    FSNewaveRepository,
)


NEWAVE_OUT_ZIP_PATTERN = "saidas_.*zip"


class AbstractNewaveUnitOfWork(ABC):
    def __enter__(self) -> "AbstractNewaveUnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def newave(self) -> AbstractNewaveRepository:
        raise NotImplementedError


class FSNewaveUnitOfWork(AbstractNewaveUnitOfWork):
    def __init__(self, path: str):
        self._current_path = Path(curdir).resolve()
        self._newave_path = path

    def __enter__(self) -> "FSNewaveUnitOfWork":
        chdir(self._newave_path)
        self._newave = FSNewaveRepository(self._newave_path)
        return super().__enter__()

    def __exit__(self, *args):
        chdir(self._current_path)
        super().__exit__(*args)

    @property
    def newave(self) -> FSNewaveRepository:
        return self._newave

    def rollback(self):
        pass


def factory(kind: str, *args, **kwargs) -> AbstractNewaveUnitOfWork:
    mappings: Dict[str, AbstractNewaveUnitOfWork] = {
        "FS": FSNewaveUnitOfWork,
    }
    return mappings[kind](*args, **kwargs)
