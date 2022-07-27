from app.services.unitofwork.newave import AbstractNewaveUnitOfWork
import app.domain.messages as messages
import app.domain.commands as commands


def process_dger_data(
    command: commands.ProcessDgerData, uow: AbstractNewaveUnitOfWork
) -> messages.DgerData:
    with uow:
        dger = uow.newave.get_dger()
        dger.considera_geracao_eolica = command.generatewind
        dger.penalidade_corte_geracao_eolica = command.windcutpenalty
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
) -> messages.PatamarData:
    with uow:
        p = uow.newave.get_patamar()
        df = p.usinas_nao_simuladas
        p.usinas_nao_simuladas = df.loc[df["Bloco"] != command.windblock, :]
        uow.newave.set_patamar(p)
        return messages.PatamarData(
            df.loc[df["Bloco"] == command.windblock, :]
        )


def process_sistema_data(
    command: commands.ProcessSistemaData,
    uow: AbstractNewaveUnitOfWork,
) -> messages.SistemaData:
    with uow:
        p = uow.newave.get_sistema()
        df = p.geracao_usinas_nao_simuladas
        p.geracao_usinas_nao_simuladas = df.loc[
            df["Bloco"] != command.windblock, :
        ]
        uow.newave.set_sistema(p)
        return messages.SistemaData(
            df.loc[df["Bloco"] == command.windblock, :]
        )


def generate_eolicacadastro(
    command: commands.GenerateEolicaCadastro, uow: AbstractNewaveUnitOfWork
):
    with uow:
        # EolicaCadastro(data=RegisterData(DefaultRegister(data="")))
        pass


def generate_eolicasubmercado(
    command: commands.GenerateEolicaSubmercado, uow: AbstractNewaveUnitOfWork
):
    with uow:
        pass


def generate_eolicaconfig(
    command: commands.GenerateEolicaConfig, uow: AbstractNewaveUnitOfWork
):
    with uow:
        pass


def generate_eolicafte(
    command: commands.GenerateEolicaFTE, uow: AbstractNewaveUnitOfWork
):
    with uow:
        pass


def generate_eolicahistorico(
    command: commands.GenerateEolicaHistorico, uow: AbstractNewaveUnitOfWork
):
    with uow:
        pass


def generate_eolicageracao(
    command: commands.GenerateEolicaGeracao, uow: AbstractNewaveUnitOfWork
):
    with uow:
        pass
