from abc import ABC, abstractmethod
from os import chdir, curdir
from typing import Dict, Type
from pathlib import Path


from app.adapters.repository.newave import (
    AbstractNewaveRepository,
    FSNewaveRepository,
)


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
    def __init__(self, path: str, caso: str, encoding_script: str):
        self._current_path = Path(curdir).resolve()
        self._newave_path = path
        self._caso = caso
        self._encoding_script = encoding_script

    def __enter__(self) -> "AbstractNewaveUnitOfWork":
        chdir(self._newave_path)
        self._newave = FSNewaveRepository(
            self._newave_path, self._caso, self._encoding_script
        )
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
    mappings: Dict[str, Type[AbstractNewaveUnitOfWork]] = {
        "FS": FSNewaveUnitOfWork,
    }
    return mappings[kind](*args, **kwargs)
