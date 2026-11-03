import streamlit as st
import pandas as pd
from dados import carregar_noticias, carregar_indicadores

st.title("📁 Upload e Download de Arquivos")

if "dados_usuario" not in st.session_state:
    st.session_state["dados_usuario"] = None

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload de CSV")
    arq = st.file_uploader("Envie um CSV com indicadores complementares", type=["csv"])
    if arq is not None:
        st.session_state["dados_usuario"] = pd.read_csv(arq)
        st.success("Arquivo carregado no Session State!")
    if st.session_state["dados_usuario"] is not None:
        st.dataframe(st.session_state["dados_usuario"])

with col2:
    st.subheader("2. Download dos Dados")
    st.download_button("📥 Baixar notícias (CSV)",
                       carregar_noticias().to_csv(index=False).encode("utf-8"),
                       "noticias_equidade.csv", "text/csv")
    st.download_button("📥 Baixar indicadores (CSV)",
                       carregar_indicadores().to_csv(index=False).encode("utf-8"),
                       "indicadores.csv", "text/csv")