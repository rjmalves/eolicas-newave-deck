from dataclasses import dataclass
import pandas as pd  # type: ignore


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
    parpmodel: int
    orderreduction: int
    generatewind: int
    windcutpenalty: float
    crosscorrelation: int
    swirlingconstraints: int
    defluenceconstraints: int


@dataclass
class ValidatePatamarData:
    windblock: int


@dataclass
class ProcessPatamarData:
    windblock: int


@dataclass
class ValidateDgerData:
    pass


@dataclass
class ValidateSistemaData:
    windblock: int


@dataclass
class ValidateInstalledCapacityData:
    initial_year: int
    final_year: int


@dataclass
class ProcessSistemaData:
    windblock: int


@dataclass
class GenerateEolicaCadastro:
    pre_study_month: int
    month: int
    year: int
    pre_study_horizon: int
    study_horizon: int
    post_study_horizon: int


@dataclass
class GenerateEolicaSubmercado:
    pass


@dataclass
class GenerateEolicaConfig:
    month: int
    year: int
    pre_study_horizon: int
    study_horizon: int
    post_study_horizon: int


@dataclass
class GenerateEolicaFTE:
    month: int
    year: int
    pre_study_horizon: int
    study_horizon: int
    post_study_horizon: int


@dataclass
class GenerateEolicaHistorico:
    pass


@dataclass
class GenerateEolicaGeracao:
    month: int
    year: int
    pre_study_horizon: int
    study_horizon: int
    post_study_horizon: int
    numblocks: int
    patamardata: pd.DataFrame
