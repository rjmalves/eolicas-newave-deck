from datetime import datetime
from dateutil.relativedelta import relativedelta  # type: ignore
from app.services.unitofwork.newave import AbstractNewaveUnitOfWork
from app.services.unitofwork.clusters import AbstractClustersUnitOfWork
from app.utils.log import Log
import pandas as pd  # type: ignore
from typing import Tuple, Optional
import app.domain.messages as messages
import app.domain.commands as commands

from cfinterface.data.registerdata import RegisterData
from cfinterface.components.defaultregister import DefaultRegister
from inewave.newave.eolicacadastro import (
    EolicaCadastro,
)
from inewave.newave.modelos.eolicacadastro import (
    RegistroEolicaCadastro,
    RegistroEolicaCadastroConjuntoAerogeradores,
    RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva,
)
from inewave.newave.eolicasubmercado import (
    EolicaSubmercado,
)
from inewave.newave.modelos.eolicasubmercado import (
    RegistroEolicaSubmercado,
)
from inewave.newave.eolicaconfiguracao import (
    EolicaConfiguracao,
)
from inewave.newave.modelos.eolicaconfiguracao import (
    RegistroEolicaConfiguracao,
)
from inewave.newave.eolicafte import (
    EolicaFTE,
)
from inewave.newave.modelos.eolicafte import (
    RegistroEolicaFTE,
)
from inewave.newave.eolicahistorico import (
    EolicaHistorico,
)
from inewave.newave.modelos.eolicahistorico import (
    RegistroEolicaHistoricoVentoHorizonte,
    RegistroEolicaHistoricoVento,
)
from inewave.newave.eolicageracao import (
    EolicaGeracao,
)
from inewave.newave.modelos.eolicageracao import (
    RegistroEolicaGeracaoPatamar,
)


def process_dger_data(
    command: commands.ProcessDgerData, uow: AbstractNewaveUnitOfWork
) -> Optional[messages.DgerData]:
    Log.log().info("Processando informações do dger.dat")
    with uow:
        dger = uow.newave.get_dger()
        dger.consideracao_media_anual_afluencias = command.parpmodel
        dger.reducao_automatica_ordem = command.orderreduction
        dger.considera_geracao_eolica = command.generatewind
        dger.penalidade_corte_geracao_eolica = command.windcutpenalty
        dger.compensacao_correlacao_cruzada = command.crosscorrelation
        dger.restricao_turbinamento = command.swirlingconstraints
        dger.restricao_defluencia = command.defluenceconstraints
        if dger.mes_inicio_estudo is None:
            Log.log().error(
                "Erro no processamento do dger.dat: não foi"
                + " encontrado valor para o campo MES INICIO ESTUDO"
            )
            return None
        if dger.ano_inicio_estudo is None:
            Log.log().error(
                "Erro no processamento do dger.dat: não foi"
                + " encontrado valor para o campo ANO INICIO ESTUDO"
            )
            return None
        if dger.num_anos_pre_estudo is None:
            Log.log().error(
                "Erro no processamento do dger.dat: não foi"
                + " encontrado valor para o campo NUM ANOS PRE ESTUDO"
            )
            return None
        if dger.num_anos_estudo is None:
            Log.log().error(
                "Erro no processamento do dger.dat: não foi"
                + " encontrado valor para o campo NUM ANOS ESTUDO"
            )
            return None
        if dger.num_anos_pos_estudo is None:
            Log.log().error(
                "Erro no processamento do dger.dat: não foi"
                + " encontrado valor para o campo NUM ANOS POS ESTUDO"
            )
            return None
        data = messages.DgerData(
            dger.mes_inicio_estudo,
            dger.ano_inicio_estudo,
            dger.num_anos_pre_estudo,
            dger.num_anos_estudo,
            dger.num_anos_pos_estudo,
        )
        uow.newave.set_dger(dger)
        return data


def process_patamar_data(
    command: commands.ProcessPatamarData,
    uow: AbstractNewaveUnitOfWork,
) -> Tuple[int, messages.PatamarData]:
    Log.log().info("Processando informações do patamar.dat")
    with uow:
        p = uow.newave.get_patamar()
        num_pat = p.numero_patamares
        assert num_pat is not None
        df = p.usinas_nao_simuladas
        assert df is not None
        p.usinas_nao_simuladas = df.loc[df["Bloco"] != command.windblock, :]
        uow.newave.set_patamar(p)
        return num_pat, messages.PatamarData(
            df.loc[df["Bloco"] == command.windblock, :]
        )


def process_sistema_data(
    command: commands.ProcessSistemaData,
    uow: AbstractNewaveUnitOfWork,
) -> messages.SistemaData:
    Log.log().info("Processando informações do sistema.dat")
    with uow:
        p = uow.newave.get_sistema()
        df = p.geracao_usinas_nao_simuladas
        assert df is not None
        p.geracao_usinas_nao_simuladas = df.loc[
            df["Bloco"] != command.windblock, :
        ]
        uow.newave.set_sistema(p)
        return messages.SistemaData(
            df.loc[df["Bloco"] == command.windblock, :]
        )


def generate_eolicacadastro(
    command: commands.GenerateEolicaCadastro,
    nw_uow: AbstractNewaveUnitOfWork,
    clusters_uow: AbstractClustersUnitOfWork,
):
    Log.log().info("Gerando arquivo eolica-cadastro.csv")
    with clusters_uow:
        clusters = clusters_uow.clusters.get_clusters()
        installed_capacity = clusters_uow.clusters.get_installed_capacity()
        installed_capacity["data_hora"] = pd.to_datetime(
            installed_capacity["data_hora"], format="%Y-%m"
        )
        installed_capacity["data_hora"] = installed_capacity[
            "data_hora"
        ].apply(lambda dt: dt.replace(day=1))
    file = EolicaCadastro(data=RegisterData(DefaultRegister(data="")))
    # Adds EOLICA-CADASTRO
    for idx, line in clusters.iterrows():
        rc = RegistroEolicaCadastro()
        rc.codigo_eolica = idx + 1
        rc.nome_eolica = str(line["cluster"])
        rc.quantidade_conjuntos = 1
        file.append_registro(rc)
    # Adds EOLICA-CADASTRO-CONJUNTO-AEROGERADORES
    for idx, line in clusters.iterrows():
        rca = RegistroEolicaCadastroConjuntoAerogeradores()
        rca.codigo_eolica = idx + 1
        rca.indice_conjunto = 1
        rca.nome_conjunto = str(line["cluster"]) + "_1"
        rca.quantidade_aerogeradores = 1
        file.append_registro(rca)
    # Adds EOLICA-CONJUNTO-AEROGERADORES-POTENCIAEFETIVA-PERIODO
    years = [command.year + i for i in range(command.study_horizon)]
    initial_months = [datetime(command.year, command.month, 1)] + [
        datetime(y, 1, 1) for y in years[1:]
    ]
    final_months = (
        [datetime(command.year, 12, 1)]
        + [datetime(y, 12, 1) for y in years[1:-1]]
        + [datetime(years[-1] + command.post_study_horizon, 12, 1)]
    )
    for idx, line in clusters.iterrows():
        for im, fm in zip(initial_months, final_months):
            rpe = RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva()
            rpe.codigo_eolica = idx + 1
            rpe.indice_conjunto = 1
            rpe.periodo_inicial = im
            rpe.periodo_final = fm
            rpe.potencia_efetiva = float(
                installed_capacity.loc[
                    (installed_capacity["cluster"] == str(line["cluster"]))
                    & (installed_capacity["data_hora"] == im),
                    "capacidade_instalada",
                ]
            )
            file.append_registro(rpe)
    with nw_uow:
        nw_uow.newave.set_eolicacadastro(file)


def generate_eolicasubmercado(
    command: commands.GenerateEolicaSubmercado,
    nw_uow: AbstractNewaveUnitOfWork,
    clusters_uow: AbstractClustersUnitOfWork,
):
    Log.log().info("Gerando arquivo eolica-submercado.csv")
    with clusters_uow:
        clusters = clusters_uow.clusters.get_clusters()
    file = EolicaSubmercado(data=RegisterData(DefaultRegister(data="")))
    for idx, line in clusters.iterrows():
        r = RegistroEolicaSubmercado()
        r.codigo_eolica = idx + 1
        r.codigo_submercado = int(line["submercado"])
        file.append_registro(r)
    with nw_uow:
        nw_uow.newave.set_eolicasubmercado(file)


def generate_eolicaconfig(
    command: commands.GenerateEolicaConfig,
    nw_uow: AbstractNewaveUnitOfWork,
    clusters_uow: AbstractClustersUnitOfWork,
):
    Log.log().info("Gerando arquivo eolica-config.csv")
    with clusters_uow:
        clusters = clusters_uow.clusters.get_clusters()
    file = EolicaConfiguracao(data=RegisterData(DefaultRegister(data="")))
    years = [command.year + i for i in range(command.study_horizon)]
    initial_month = datetime(command.year, command.month, 1)
    final_month = datetime(years[-1] + command.post_study_horizon, 12, 1)
    for idx, _ in clusters.iterrows():
        r = RegistroEolicaConfiguracao()
        r.codigo_eolica = idx + 1
        r.data_inicial_estado_operacao = initial_month
        r.data_final_estado_operacao = final_month
        r.estado_operacao = "centralizado"
        file.append_registro(r)
    with nw_uow:
        nw_uow.newave.set_eolicaconfiguracao(file)


def generate_eolicafte(
    command: commands.GenerateEolicaFTE,
    nw_uow: AbstractNewaveUnitOfWork,
    clusters_uow: AbstractClustersUnitOfWork,
):
    Log.log().info("Gerando arquivo eolica-fte.csv")
    with clusters_uow:
        ftm = clusters_uow.clusters.get_ftm()
    with nw_uow:
        eolicacadastro = nw_uow.newave.get_eolicacadastro()
    file = EolicaFTE(data=RegisterData(DefaultRegister(data="")))
    initial_month = datetime(command.year, command.month, 1)
    final_month = datetime(
        command.year + command.study_horizon + command.post_study_horizon - 1,
        12,
        1,
    )
    for _, line in ftm.iterrows():
        r = RegistroEolicaFTE()
        rc = eolicacadastro.eolica_cadastro(nome_eolica=str(line["cluster"]))
        assert isinstance(rc, RegistroEolicaCadastro)
        r.codigo_eolica = rc.codigo_eolica
        r.data_inicial = initial_month
        r.data_final = final_month
        r.coeficiente_linear = float(line["b0"])
        r.coeficiente_angular = float(line["b1"])
        file.append_registro(r)
    with nw_uow:
        nw_uow.newave.set_eolicafte(file)


def generate_eolicahistorico(
    command: commands.GenerateEolicaHistorico,
    nw_uow: AbstractNewaveUnitOfWork,
    clusters_uow: AbstractClustersUnitOfWork,
):
    Log.log().info("Gerando arquivo hist-ventos.csv")
    with clusters_uow:
        clusters = clusters_uow.clusters.get_clusters()
        history = clusters_uow.clusters.get_average_wind()
        history["data_hora"] = pd.to_datetime(
            history["data_hora"], format="%Y-%m-%d"
        )
    with nw_uow:
        eolicacadastro = nw_uow.newave.get_eolicacadastro()
    file = EolicaHistorico(data=RegisterData(DefaultRegister(data="")))
    first_january = [h for h in history["data_hora"] if h.month == 1][0]
    last_january = [h for h in history["data_hora"] if h.month == 1][-1]
    considered_history = history.loc[
        (history["data_hora"] >= first_january)
        & (history["data_hora"] <= last_january),
        :,
    ]

    rh = RegistroEolicaHistoricoVentoHorizonte()
    rh.data_inicial = first_january
    rh.data_final = last_january
    file.append_registro(rh)

    for _, clusterline in clusters.iterrows():
        clustername = str(clusterline["cluster"])
        rc = eolicacadastro.eolica_cadastro(nome_eolica=clustername)
        assert isinstance(rc, RegistroEolicaCadastro)
        code = rc.codigo_eolica
        clusterhistory = considered_history.loc[
            considered_history["cluster"] == clustername, :
        ]
        for _, line in clusterhistory.iterrows():
            r = RegistroEolicaHistoricoVento()
            r.codigo_eolica = code
            r.data_inicial = line["data_hora"]
            r.data_final = line["data_hora"] + relativedelta(months=1)
            r.velocidade = line["vento"]
            r.direcao = 0.0
            file.append_registro(r)
    with nw_uow:
        nw_uow.newave.set_histventos(file)


def generate_eolicageracao(
    command: commands.GenerateEolicaGeracao,
    nw_uow: AbstractNewaveUnitOfWork,
    clusters_uow: AbstractClustersUnitOfWork,
):

    MONTHS = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    Log.log().info("Gerando arquivo eolica-geracao.csv")

    with clusters_uow:
        clusters = clusters_uow.clusters.get_clusters()

    with nw_uow:
        eolicacadastro = nw_uow.newave.get_eolicacadastro()
        eolicasubmercado = nw_uow.newave.get_eolicasubmercado()

    file = EolicaGeracao(data=RegisterData(DefaultRegister(data="")))
    numblocks = command.numblocks
    blocks = list(range(1, numblocks + 1))
    blockdepths = command.patamardata
    years = [
        command.year + i
        for i in range(command.study_horizon + command.post_study_horizon)
    ]

    for _, clusterline in clusters.iterrows():
        clustername = str(clusterline["cluster"])
        rc = eolicacadastro.eolica_cadastro(nome_eolica=clustername)
        assert isinstance(rc, RegistroEolicaCadastro)
        code = rc.codigo_eolica
        rs = eolicasubmercado.eolica_submercado(codigo_eolica=code)
        assert isinstance(rs, RegistroEolicaSubmercado)
        sub = rs.codigo_submercado
        df = blockdepths.copy()
        df_sub = df.loc[df["Subsistema"] == sub, MONTHS + ["Ano"]]
        df_sub["Patamar"] = blocks * command.study_horizon
        for year in years:
            # freezes the year in the last study year
            consulting_year = min(
                [command.year + command.study_horizon - 1, year]
            )
            for m, month in enumerate(MONTHS, start=1):
                for b in blocks:
                    d = datetime(year=year, month=m, day=1)
                    r = RegistroEolicaGeracaoPatamar()
                    r.codigo_eolica = code
                    r.data_inicial = d
                    r.data_final = d
                    r.indice_patamar = b
                    r.profundidade = float(
                        df_sub.loc[
                            (df_sub["Ano"] == consulting_year)
                            & (df_sub["Patamar"] == b),
                            month,
                        ]
                    )
                    file.append_registro(r)

    with nw_uow:
        nw_uow.newave.set_eolicageracao(file)
