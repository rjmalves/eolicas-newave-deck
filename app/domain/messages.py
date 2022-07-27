from dataclasses import dataclass
import pandas as pd


@dataclass
class DgerData:
    month: int
    year: int
    pre_study_horizon: int
    study_horizon: int
    post_study_horizon: int


@dataclass
class PatamarData:
    blocks: pd.DataFrame


@dataclass
class SistemaData:
    nonsimulated: pd.DataFrame
