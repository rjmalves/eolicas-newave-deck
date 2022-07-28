from abc import ABC, abstractmethod
from os import chdir, curdir
import re
from typing import Dict
from pathlib import Path


from app.adapters.repository.clusters import (
    AbstractClustersRepository,
    FSClustersRepository,
)


class AbstractClustersUnitOfWork(ABC):
    def __enter__(self) -> "AbstractClustersUnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def clusters(self) -> AbstractClustersRepository:
        raise NotImplementedError


class FSClustersUnitOfWork(AbstractClustersUnitOfWork):
    def __init__(
        self,
        path: str,
        clusters_file: str,
        installed_capacity_file: str,
        ftm_file: str,
        average_wind_file: str,
    ):
        self._current_path = Path(curdir).resolve()
        self._clusters_path = path
        self._clusters_file = clusters_file
        self._installed_capacity_file = installed_capacity_file
        self._ftm_file = ftm_file
        self._average_wind_file = average_wind_file

    def __enter__(self) -> "FSClustersUnitOfWork":
        chdir(self._clusters_path)
        self._clusters = FSClustersRepository(
            self._clusters_file,
            self._installed_capacity_file,
            self._ftm_file,
            self._average_wind_file,
        )
        return super().__enter__()

    def __exit__(self, *args):
        chdir(self._current_path)
        super().__exit__(*args)

    @property
    def clusters(self) -> FSClustersRepository:
        return self._clusters

    def rollback(self):
        pass


def factory(kind: str, *args, **kwargs) -> AbstractClustersUnitOfWork:
    mappings: Dict[str, AbstractClustersUnitOfWork] = {
        "FS": FSClustersUnitOfWork,
    }
    return mappings[kind](*args, **kwargs)
