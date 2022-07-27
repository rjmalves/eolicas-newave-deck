from dataclasses import dataclass
import pandas as pd


@dataclass
class ExtractZipFile:
    zippath: str
    targetdir: str
    filename: str


@dataclass
class AddFileToZip:
    zippath: str
    srcdir: str
    filename: str


@dataclass
class ProcessDgerData:
    generatewind: int
    windcutpenalty: float


@dataclass
class ProcessPatamarData:
    windblock: int


@dataclass
class ProcessSistemaData:
    windblock: int


@dataclass
class GenerateEolicaCadastro:
    month: int
    year: int
    pre_study_horizon: int
    study_horizon: int
    post_study_horizon: int
    clustersdir: str
    clustersfile: str
    installedcapacityfile: str
    tmpdir: str
    outputfile: str


@dataclass
class GenerateEolicaSubmercado:
    clustersdir: str
    clustersfile: str
    tmpdir: str
    eolicacadastrofile: str
    outputfile: str


@dataclass
class GenerateEolicaConfig:
    month: int
    year: int
    pre_study_horizon: int
    study_horizon: int
    post_study_horizon: int
    clustersdir: str
    clustersfile: str
    tmpdir: str
    eolicacadastrofile: str
    outputfile: str


@dataclass
class GenerateEolicaFTE:
    month: int
    year: int
    pre_study_horizon: int
    study_horizon: int
    post_study_horizon: int
    clustersdir: str
    ftmfile: str
    tmpdir: str
    eolicacadastrofile: str
    outputfile: str


@dataclass
class GenerateEolicaHistorico:
    clustersdir: str
    averagewindfile: str
    tmpdir: str
    eolicacadastrofile: str
    outputfile: str


@dataclass
class GenerateEolicaGeracao:
    month: int
    year: int
    pre_study_horizon: int
    study_horizon: int
    post_study_horizon: int
    patamardata: pd.DataFrame
    tmpdir: str
    eolicacadastrofile: str
    eolicasubmercadofile: str
    outputfile: str
