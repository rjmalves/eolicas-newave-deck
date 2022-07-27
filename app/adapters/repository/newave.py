from abc import ABC, abstractmethod
from typing import Dict

from inewave.newave.caso import Caso
from inewave.newave.arquivos import Arquivos
from inewave.newave.dger import DGer
from inewave.newave.patamar import Patamar
from inewave.newave.sistema import Sistema
from inewave.newave.eolicacadastro import EolicaCadastro
from inewave.newave.eolicaconfiguracao import EolicaConfiguracao
from inewave.newave.eolicasubmercado import EolicaSubmercado
from inewave.newave.eolicafte import EolicaFTE
from inewave.newave.eolicahistorico import EolicaHistorico
from inewave.newave.eolicageracao import EolicaGeracao

from cfinterface.components.defaultregister import DefaultRegister
from cfinterface.data.registerdata import RegisterData


class AbstractNewaveRepository(ABC):
    @abstractmethod
    @property
    def caso(self) -> Caso:
        raise NotImplementedError

    @abstractmethod
    @property
    def arquivos(self) -> Arquivos:
        raise NotImplementedError

    @abstractmethod
    def get_dger(self) -> DGer:
        raise NotImplementedError

    @abstractmethod
    def set_dger(self, d: DGer):
        raise NotImplementedError

    @abstractmethod
    def get_patamar(self) -> Patamar:
        raise NotImplementedError

    @abstractmethod
    def set_patamar(self, d: Patamar):
        raise NotImplementedError

    @abstractmethod
    def get_sistema(self) -> Sistema:
        raise NotImplementedError

    @abstractmethod
    def set_sistema(self, d: Sistema):
        raise NotImplementedError

    @abstractmethod
    def get_eolicacadastro(self) -> EolicaCadastro:
        raise NotImplementedError

    @abstractmethod
    def set_eolicacadastro(self, d: EolicaCadastro):
        raise NotImplementedError

    @abstractmethod
    def set_eolicaconfiguracao(self, d: EolicaConfiguracao):
        raise NotImplementedError

    @abstractmethod
    def get_eolicasubmercado(self) -> EolicaSubmercado:
        raise NotImplementedError

    @abstractmethod
    def set_eolicasubmercado(self, d: EolicaSubmercado):
        raise NotImplementedError

    @abstractmethod
    def set_eolicafte(self, d: EolicaFTE):
        raise NotImplementedError

    @abstractmethod
    def set_eolicageracao(self, d: EolicaGeracao):
        raise NotImplementedError

    @abstractmethod
    def set_histventos(self, d: EolicaHistorico):
        raise NotImplementedError


class FSNewaveRepository(AbstractNewaveRepository):
    def __init__(self, path: str):
        self.__path = path
        self.__caso = Caso.le_arquivo(self.__path)
        self.__arquivos = None

    @property
    def caminho(self) -> str:
        return self.__path

    @property
    def caso(self) -> Caso:
        return self.__caso

    @property
    def arquivos(self) -> Arquivos:
        if self.__arquivos is None:
            self.__arquivos = Arquivos.le_arquivo(
                self.__path, self.__caso.arquivos
            )
        return self.__arquivos

    def get_dger(self) -> DGer:
        return DGer.le_arquivo(self.__path, self.arquivos.dger)

    def set_dger(self, d: DGer):
        d.escreve_arquivo(self.__path, self.__arquivos.dger)

    def get_patamar(self) -> Patamar:
        return Patamar.le_arquivo(self.__path, self.arquivos.patamar)

    def set_patamar(self, d: Patamar):
        d.escreve_arquivo(self.__path, self.__arquivos.patamar)

    def get_sistema(self) -> Sistema:
        return Sistema.le_arquivo(self.__path, self.arquivos.sistema)

    def set_sistema(self, d: Sistema):
        d.escreve_arquivo(self.__path, self.__arquivos.sistema)


def factory(kind: str, *args, **kwargs) -> AbstractNewaveRepository:
    mapping: Dict[str, AbstractNewaveRepository] = {
        "FS": FSNewaveRepository(*args, **kwargs)
    }
    return mapping[kind]
