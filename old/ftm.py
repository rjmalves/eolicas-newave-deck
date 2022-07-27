from datetime import datetime
import pandas as pd
from os.path import join
from inewave.newave.eolicafte import (
    EolicaFTE,
)
from inewave.newave.eolicacadastro import (
    EolicaCadastro,
)
from inewave.newave.modelos.eolicafte import (
    RegistroEolicaFTE,
)

DIR_CASO = "./NE_kmeans2_S_kmeans1"
DIR_FTE = join(DIR_CASO, "deck")
ARQ_FTE = "eolica-fte.csv"
ARQ_CADSTRO = "eolica-cadastro.csv"
ARQ_FTM = "ftm.csv"
ANO_ESTUDO = 2021

df_ftm = pd.read_csv(join(DIR_CASO, ARQ_FTM))
fte = EolicaFTE.le_arquivo(DIR_FTE, ARQ_FTE)
cadastro = EolicaCadastro.le_arquivo(DIR_FTE, ARQ_CADSTRO)

clusters = df_ftm["Cluster"].unique().tolist()
for c in clusters:
    codigo_cluster = cadastro.eolica_cadastro(nome_eolica=c).codigo_eolica
    p_inicial = datetime(ANO_ESTUDO, 1, 1)
    p_final = datetime(ANO_ESTUDO + 9, 12, 1)

    if (
        fte.eolica_funcao_producao(
            codigo_eolica=codigo_cluster,
            data_inicial=p_inicial,
        )
        is None
    ):
        r = RegistroEolicaFTE()
        r.codigo_eolica = codigo_cluster
        r.data_inicial = p_inicial
        r.data_final = p_final
        r.coeficiente_linear = float(
            df_ftm.loc[
                df_ftm["Cluster"] == c,
                "b0",
            ]
        )
        r.coeficiente_angular = float(
            df_ftm.loc[
                df_ftm["Cluster"] == c,
                "b1",
            ]
        )
        fte.append_registro(r)

fte.escreve_arquivo(DIR_FTE, ARQ_FTE)
