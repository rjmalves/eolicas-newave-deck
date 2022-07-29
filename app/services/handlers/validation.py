from app.services.unitofwork.newave import AbstractNewaveUnitOfWork
from app.services.unitofwork.clusters import AbstractClustersUnitOfWork
from app.utils.log import Log
import app.domain.commands as commands


def validate_patamar_data(
    command: commands.ValidatePatamarData,
    uow: AbstractNewaveUnitOfWork,
) -> bool:
    Log.log().info("Validando informações do patamar.dat")
    with uow:
        p = uow.newave.get_patamar()
        df = p.usinas_nao_simuladas
        if df is None:
            Log.log().error(
                "Arquivo patamar.dat não contém"
                + " informações dos patamares de geração"
            )
            return False
        p.usinas_nao_simuladas = df.loc[df["Bloco"] != command.windblock, :]
        winddata = df.loc[df["Bloco"] == command.windblock, :]
        if winddata.empty:
            Log.log().error(
                "Arquivo patamar.dat não contém"
                + " informações dos patamares de geração eólica"
                + f" (bloco {command.windblock})"
            )
            return False
        else:
            Log.log().info("Arquivo patamar.dat validado com sucesso")
            return True


def validate_sistema_data(
    command: commands.ValidateSistemaData,
    uow: AbstractNewaveUnitOfWork,
) -> bool:
    Log.log().info("Validando informações do sistema.dat")
    with uow:
        p = uow.newave.get_sistema()
        df = p.geracao_usinas_nao_simuladas
        if df is None:
            Log.log().error(
                "Arquivo sistema.dat não contém"
                + " informações de geração não simulada"
            )
            return False
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
            return False
        else:
            Log.log().info("Arquivo sistema.dat validado com sucesso")
            return True


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
