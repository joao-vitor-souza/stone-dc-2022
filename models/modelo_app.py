import warnings

import pandas as pd
import streamlit as st

from utils.gerador import Gerador
from utils.plots import Plots

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Modelo Sazonal", page_icon="📊")

"---"
st.header("Modelo Sazonal")

dados = pd.read_parquet("../data/processed/geralTpvLimpo.parquet")

col_1, col_2 = st.columns(2)

contrato_id = col_1.selectbox("ID do contrato", dados.contrato_id.unique())

status_ativo = col_2.radio(
    "Somente o estado ativo do contrato?", options=["Sim", "Não"]
)

status_ativo = True if status_ativo == "Sim" else False

chamada = col_1.button("Gerar Modelo")

if chamada:

    gerador = Gerador()
    dadosSazonalidade = gerador.dadosSazonalidade(
        dados, contrato_id=contrato_id, status_ativo=status_ativo
    )

    grafico = Plots(dadosSazonalidade)
    grafico.gerarCurvaSazonalidade()
    sazonalidade, sazonalidadeComponentes = grafico.graficos

    st.plotly_chart(sazonalidade, use_container_width=True)
    st.plotly_chart(sazonalidadeComponentes, use_container_width=True)

"---"
