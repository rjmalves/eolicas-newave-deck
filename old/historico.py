from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from os.path import join
from inewave.newave.eolicahistorico import (
    EolicaHistorico,
)
from inewave.newave.eolicacadastro import (
    EolicaCadastro,
)
from inewave.newave.modelos.eolicahistorico import (
    RegistroEolicaHistoricoVento,
)

DIR_CASO = "./NE_kmeans2_S_kmeans1"
DIR_HISTORICO = join(DIR_CASO, "deck")
ARQ_HISTORICO = "hist-ventos.csv"
ARQ_CADASTRO = "eolica-cadastro.csv"
ARQ_VENTO_MEDIO = "vento_medio.csv"

df_hist = pd.read_csv(join(DIR_CASO, ARQ_VENTO_MEDIO))
df_hist["data_hora"] = pd.to_datetime(df_hist["data_hora"], format="%Y-%m-%d")
hist = EolicaHistorico.le_arquivo(DIR_HISTORICO, ARQ_HISTORICO)
cadastro = EolicaCadastro.le_arquivo(DIR_HISTORICO, ARQ_CADASTRO)

# TODO - adicionar regra de que tem que começar em janeiro e terminar em dezembro
clusters = df_hist["Cluster"].unique().tolist()
for c in clusters:
    codigo_cluster = cadastro.eolica_cadastro(nome_eolica=c).codigo_eolica
    datas = df_hist.loc[df_hist["Cluster"] == c, "data_hora"].tolist()
    for d in datas:
        if (
            hist.eolica_historico_vento(
                codigo_eolica=codigo_cluster,
                data_inicial=d,
            )
            is None
        ):
            r = RegistroEolicaHistoricoVento()
            r.codigo_eolica = codigo_cluster
            r.data_inicial = d
            r.data_final = d + relativedelta(months=1)
            r.velocidade = float(
                df_hist.loc[
                    (df_hist["Cluster"] == c) & (df_hist["data_hora"] == d),
                    "vento_medio",
                ]
            )
            r.direcao = 0.0
            hist.append_registro(r)

hist.escreve_arquivo(DIR_HISTORICO, ARQ_HISTORICO)
