from abc import ABC, abstractmethod
from typing import Dict
import pathlib
from app.utils.encoding import convert_encoding

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


class AbstractNewaveRepository(ABC):
    @property
    @abstractmethod
    def caso(self) -> Caso:
        raise NotImplementedError

    @property
    @abstractmethod
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
    def __init__(self, path: pathlib.Path, caso: str, encoding_script: str):
        self.__path = path
        self.__caso = Caso.le_arquivo(self.__path, caso)
        self.__encoding_script = encoding_script
        self.__arquivos = None

    @property
    def caminho(self) -> pathlib.Path:
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
        convert_encoding(
            self.__path.joinpath(self.arquivos.dger), self.__encoding_script
        )
        return DGer.le_arquivo(self.__path, self.arquivos.dger)

    def set_dger(self, d: DGer):
        d.escreve_arquivo(self.__path, self.__arquivos.dger)

    def get_patamar(self) -> Patamar:
        convert_encoding(
            self.__path.joinpath(self.arquivos.patamar), self.__encoding_script
        )
        return Patamar.le_arquivo(self.__path, self.arquivos.patamar)

    def set_patamar(self, d: Patamar):
        d.escreve_arquivo(self.__path, self.__arquivos.patamar)

    def get_sistema(self) -> Sistema:
        convert_encoding(
            self.__path.joinpath(self.arquivos.sistema), self.__encoding_script
        )
        return Sistema.le_arquivo(self.__path, self.arquivos.sistema)

    def set_sistema(self, d: Sistema):
        d.escreve_arquivo(self.__path, self.__arquivos.sistema)

    def get_eolicacadastro(self) -> EolicaCadastro:
        return EolicaCadastro.le_arquivo(self.__path, "eolica-cadastro.csv")

    def set_eolicacadastro(self, d: EolicaCadastro):
        d.escreve_arquivo(self.__path, "eolica-cadastro.csv")

    def set_eolicaconfiguracao(self, d: EolicaConfiguracao):
        d.escreve_arquivo(self.__path, "eolica-config.csv")

    def get_eolicasubmercado(self) -> EolicaSubmercado:
        return EolicaSubmercado.le_arquivo(
            self.__path, "eolica-submercado.csv"
        )

    def set_eolicasubmercado(self, d: EolicaSubmercado):
        d.escreve_arquivo(self.__path, "eolica-submercado.csv")

    def set_eolicafte(self, d: EolicaFTE):
        d.escreve_arquivo(self.__path, "eolica-fte.csv")

    def set_eolicageracao(self, d: EolicaGeracao):
        d.escreve_arquivo(self.__path, "eolica-geracao.csv")

    def set_histventos(self, d: EolicaHistorico):
        d.escreve_arquivo(self.__path, "hist-ventos.csv")


def factory(kind: str, *args, **kwargs) -> AbstractNewaveRepository:
    mapping: Dict[str, AbstractNewaveRepository] = {
        "FS": FSNewaveRepository(*args, **kwargs)
    }
    return mapping[kind]
