from app.services.unitofwork.newave import AbstractNewaveUnitOfWork
from app.services.unitofwork.clusters import AbstractClustersUnitOfWork
from app.utils.log import Log
import app.domain.commands as commands
import pandas as pd  # type: ignore
from typing import Optional, Tuple


def validate_dger_data(
    command: commands.ValidateDgerData,
    uow: AbstractNewaveUnitOfWork,
) -> Tuple[Optional[int], Optional[int]]:
    Log.log().info("Validando informações do dger.dat")
    with uow:
        d = uow.newave.get_dger()
        initial_year = d.ano_inicio_estudo - d.num_anos_pre_estudo
        final_year = (
            d.ano_inicio_estudo + d.num_anos_estudo + d.num_anos_pos_estudo
        )
        if initial_year is None or final_year is None:
            Log.log().error(
                "Arquivo dger.dat não contém" + "as informações necessárias"
            )
        else:
            Log.log().info("Arquivo dger.dat validado com sucesso")
            return [initial_year, final_year]


def validate_patamar_data(
    command: commands.ValidatePatamarData,
    uow: AbstractNewaveUnitOfWork,
) -> Optional[pd.DataFrame]:
    Log.log().info("Validando informações do patamar.dat")
    with uow:
        p = uow.newave.get_patamar()
        df = p.usinas_nao_simuladas
        if df is None:
            Log.log().error(
                "Arquivo patamar.dat não contém"
                + " informações dos patamares de geração"
            )
            return None
        p.usinas_nao_simuladas = df.loc[df["Bloco"] != command.windblock, :]
        winddata = df.loc[df["Bloco"] == command.windblock, :]
        if winddata.empty:
            Log.log().error(
                "Arquivo patamar.dat não contém"
                + " informações dos patamares de geração eólica"
                + f" (bloco {command.windblock})"
            )
            return None
        else:
            Log.log().info("Arquivo patamar.dat validado com sucesso")
            return winddata


def validate_sistema_data(
    command: commands.ValidateSistemaData,
    uow: AbstractNewaveUnitOfWork,
) -> Optional[pd.DataFrame]:
    Log.log().info("Validando informações do sistema.dat")
    with uow:
        p = uow.newave.get_sistema()
        df = p.geracao_usinas_nao_simuladas
        if df is None:
            Log.log().error(
                "Arquivo sistema.dat não contém"
                + " informações de geração não simulada"
            )
            return None
        p.geracao_usinas_nao_simuladas = df.loc[
            df["Bloco"] != command.windblock, :
        ]
        winddata = df.loc[df["Bloco"] == command.windblock, :]
        if winddata.empty:
            Log.log().error(
                "Arquivo sistema.dat não contém"
                + " informações de geração eólica não simulada"
                + f" (bloco {command.windblock})"
            )
            return None
        else:
            Log.log().info("Arquivo sistema.dat validado com sucesso")
            return winddata


def validate_cluster_files(clusters_uow: AbstractClustersUnitOfWork) -> bool:
    try:
        with clusters_uow:
            clusters = clusters_uow.clusters.get_clusters()
            installed_capacity = clusters_uow.clusters.get_installed_capacity()
            ftm = clusters_uow.clusters.get_ftm()
            average_wind = clusters_uow.clusters.get_average_wind()
    except Exception as e:
        Log.log().exception(
            "Erro na leitura dos arquivos com dados"
            + f" da clusterização de usinas eólicas: {e}"
        )
        return False

    if any(
        [df.empty for df in [clusters, installed_capacity, ftm, average_wind]]
    ):
        Log.log().error(
            "Arquivos com dados da clusterização de usinas eólicas"
            + " estão incompletos"
        )
        return False
    else:
        Log.log().info(
            "Arquivos com dados de clusterização de usinas"
            + " eólicas validados com sucesso"
        )
        return True


def validate_cluster_file(clusters_uow: AbstractClustersUnitOfWork) -> bool:
    try:
        with clusters_uow:
            clusters = clusters_uow.clusters.get_clusters()
    except Exception as e:
        Log.log().exception(
            "Erro na leitura do arquivo com "
            + f" clusters de usinas eólicas: {e}"
        )

    colunas = ["cluster", "submercado"]
    if not all([c in clusters.columns for c in colunas]):
        Log.log().error(
            "Arquivo com clusters de usinas eólicas"
            + f" não possui as colunas: {colunas}"
        )
        return False
    else:
        Log.log().info(
            "Arquivo com clusters de usinas " + "eólicas validado com sucesso"
        )
        return True


def validate_installed_capacity_file(
    command: commands.ValidateInstalledCapacityData,
    clusters_uow: AbstractClustersUnitOfWork,
) -> bool:
    try:
        with clusters_uow:
            installed_capacity = clusters_uow.clusters.get_installed_capacity()
    except Exception as e:
        Log.log().exception(
            "Erro na leitura do arquivo com "
            + f" capacidades instaladas de clusters: {e}"
        )
        return False

    colunas = ["cluster", "capacidade_instalada", "data_hora"]
    if not all([c in installed_capacity.columns for c in colunas]):
        Log.log().error(
            "Arquivo com capacidades instaladas de clusters de usinas eólicas"
            + f" não possui as colunas: {colunas}"
        )
        return False
    else:
        dt = pd.to_datetime(installed_capacity["data_hora"], format="%Y-%m-%d")
        if command.initial_year < dt.min().year:
            Log.log().warning(
                "Arquivo com capacidades instaladas de clusters de usinas "
                + f"começa no ano {dt.min().year} > {command.initial_year}"
            )
        if command.final_year > dt.max().year:
            Log.log().warning(
                "Arquivo com capacidades instaladas de clusters de usinas "
                + f"termina no ano {dt.max().year} < {command.final_year} "
            )

        Log.log().info(
            "Arquivo com capacidades instaladas de clusters de usinas "
            + "eólicas validado com sucesso"
        )
        return True


def validate_ftm_file(
    clusters_uow: AbstractClustersUnitOfWork,
) -> bool:
    try:
        with clusters_uow:
            ftms = clusters_uow.clusters.get_ftm()
    except Exception as e:
        Log.log().exception(
            "Erro na leitura do arquivo com " + f" FTMs de clusters: {e}"
        )

    colunas = ["cluster", "b0", "b1"]
    if not all([c in ftms.columns for c in colunas]):
        Log.log().error(
            "Arquivo com FTMs de clusters de usinas eólicas"
            + f" não possui as colunas: {colunas}"
        )
        return False
    else:
        Log.log().info(
            "Arquivo com FTMs de clusters de usinas "
            + "eólicas validado com sucesso"
        )
        return True


def validate_average_wind_file(
    clusters_uow: AbstractClustersUnitOfWork,
) -> bool:
    try:
        with clusters_uow:
            average_wind = clusters_uow.clusters.get_average_wind()
    except Exception as e:
        Log.log().exception(
            "Erro na leitura do arquivo com "
            + f" vento médio de clusters: {e}"
        )

    colunas = ["cluster", "vento", "data_hora"]
    if not all([c in average_wind.columns for c in colunas]):
        Log.log().error(
            "Arquivo com vento médio de clusters de usinas eólicas"
            + f" não possui as colunas: {colunas}"
        )
        return False
    else:
        Log.log().info(
            "Arquivo com vento médio de clusters de usinas "
            + "eólicas validado com sucesso"
        )
        return True
