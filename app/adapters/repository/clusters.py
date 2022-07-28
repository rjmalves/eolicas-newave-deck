from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd


class AbstractClustersRepository(ABC):
    @abstractmethod
    def get_clusters(self) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_installed_capacity(self) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_ftm(self) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_average_wind(self) -> pd.DataFrame:
        raise NotImplementedError


class FSClustersRepository(AbstractClustersRepository):
    def __init__(
        self,
        clusters_file: str,
        installed_capacity_file: str,
        ftm_file: str,
        average_wind_file: str,
    ):
        self.__clusters_file = clusters_file
        self.__installed_capacity_file = installed_capacity_file
        self.__ftm_file = ftm_file
        self.__average_wind_file = average_wind_file
        self.__clusters = None
        self.__installed_capacity = None
        self.__ftm = None
        self.__average_wind = None

    def get_clusters(self) -> pd.DataFrame:
        if self.__clusters is None:
            self.__clusters = pd.read_csv(self.__clusters_file, index_col=None)
        return self.__clusters

    def get_ftm(self) -> pd.DataFrame:
        if self.__ftm is None:
            self.__ftm = pd.read_csv(self.__ftm_file, index_col=None)
        return self.__ftm

    def get_installed_capacity(self) -> pd.DataFrame:
        if self.__installed_capacity is None:
            self.__installed_capacity = pd.read_csv(
                self.__installed_capacity_file,
                index_col=None,
            )
        return self.__installed_capacity

    def get_average_wind(self) -> pd.DataFrame:
        if self.__average_wind is None:
            self.__average_wind = pd.read_csv(
                self.__average_wind_file, index_col=None
            )
        return self.__average_wind


def factory(kind: str, *args, **kwargs) -> AbstractClustersRepository:
    mapping: Dict[str, AbstractClustersRepository] = {
        "FS": FSClustersRepository(*args, **kwargs)
    }
    return mapping[kind]
