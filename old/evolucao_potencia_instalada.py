from datetime import datetime
import pandas as pd
from os.path import join
from inewave.newave.eolicacadastro import (
    EolicaCadastro,
)
from inewave.newave.modelos.eolicacadastro import (
    RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva,
)

DIR_CASO = "./NE_kmeans2_S_kmeans1"
DIR_CADASTRO = join(DIR_CASO, "deck")
ARQ_CADASTRO = "eolica-cadastro.csv"
ARQ_CAPACIDADE = "capinst_acum_cluster.csv"
ANO_INICIAL = 2021

df_capacidade = pd.read_csv(join(DIR_CASO, ARQ_CAPACIDADE))
cadastro = EolicaCadastro.le_arquivo(DIR_CADASTRO, ARQ_CADASTRO)

df_capacidade["Data"] = pd.to_datetime(df_capacidade["Data"], format="%Y-%m")

anos = [2021 + i for i in range(5)]
clusters = df_capacidade["Cluster"].unique().tolist()
for c in clusters:
    codigo_cluster = cadastro.eolica_cadastro(nome_eolica=c).codigo_eolica
    for a in anos:
        p_inicial = datetime(a, 1, 1)
        p_final = (
            datetime(a, 12, 1)
            if a != anos[-1]
            else datetime(anos[0] + 9, 12, 1)
        )
        if (
            cadastro.eolica_conjunto_aerogeradores_potencia_efetiva_periodo(
                codigo_eolica=codigo_cluster,
                indice_conjunto=1,
                periodo_inicial=p_inicial,
            )
            is None
        ):
            r = RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva()
            r.codigo_eolica = codigo_cluster
            r.indice_conjunto = 1
            r.periodo_inicial = p_inicial
            r.periodo_final = p_final
            r.potencia_efetiva = float(
                df_capacidade.loc[
                    (df_capacidade["Cluster"] == c)
                    & (df_capacidade["Data"] == p_inicial),
                    "CapInst_acum",
                ]
            )
            cadastro.append_registro(r)

cadastro.escreve_arquivo(DIR_CADASTRO, ARQ_CADASTRO)
