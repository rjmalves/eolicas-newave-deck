from datetime import datetime

from os.path import join
from inewave.newave.eolicageracao import (
    EolicaGeracao,
)
from inewave.newave.eolicasubmercado import (
    EolicaSubmercado,
)
from inewave.newave.eolicacadastro import (
    EolicaCadastro,
)
from inewave.newave.modelos.eolicageracao import (
    RegistroEolicaGeracaoPatamar,
)
from inewave.newave.patamar import Patamar
from inewave.config import MESES_DF

DIR_CASO = "./NE_kmeans3_S_kmeans2"
DIR_GERACAO = join(DIR_CASO, "deck")
ARQ_GERACAO = "eolica-geracao.csv"
ARQ_CADASTRO = "eolica-cadastro.csv"
ARQ_SUBMERCADO = "eolica-submercado.csv"
ARQ_PATAMAR = "patamar.dat"
ANOS_ESTUDO = 5

cadastro = EolicaCadastro.le_arquivo(DIR_GERACAO, ARQ_CADASTRO)
submercado = EolicaSubmercado.le_arquivo(DIR_GERACAO, ARQ_SUBMERCADO)
geracao = EolicaGeracao.le_arquivo(DIR_GERACAO, ARQ_GERACAO)

patamar = Patamar.le_arquivo(DIR_GERACAO, ARQ_PATAMAR)

PATAMARES = list(range(1, patamar.numero_patamares + 1))

clusters = [r.nome_eolica for r in cadastro.eolica_cadastro()]

for c in clusters:
    codigo_cluster = cadastro.eolica_cadastro(nome_eolica=c).codigo_eolica
    submercado_cluster = submercado.eolica_submercado(
        codigo_eolica=codigo_cluster
    ).codigo_submercado
    eol = patamar.usinas_nao_simuladas
    df_eol = eol.loc[
        (eol["Subsistema"] == submercado_cluster) & (eol["Bloco"] == 3),
        MESES_DF + ["Ano"],
    ]
    df_eol["Patamar"] = PATAMARES * ANOS_ESTUDO
    ano_inicial = df_eol["Ano"].unique().tolist()[0]
    anos = list(range(ano_inicial, ano_inicial + 10))
    for a in anos:
        for m, mes in enumerate(MESES_DF, start=1):
            for p in PATAMARES:
                d = datetime(year=a, month=m, day=1)
                if (
                    geracao.eolica_geracao_profundidade_periodo_patamar(
                        codigo_eolica=codigo_cluster,
                        data_inicial=d,
                        indice_patamar=p,
                    )
                    is None
                ):
                    r = RegistroEolicaGeracaoPatamar()
                    r.codigo_eolica = codigo_cluster
                    r.data_inicial = d
                    r.data_final = d
                    r.indice_patamar = p
                    ano_indice = a if a <= ano_inicial + 4 else ano_inicial + 4
                    r.profundidade = float(
                        df_eol.loc[
                            (df_eol["Ano"] == ano_indice)
                            & (df_eol["Patamar"] == p),
                            mes,
                        ]
                    )
                    geracao.append_registro(r)

geracao.escreve_arquivo(DIR_GERACAO, ARQ_GERACAO)
