import streamlit as st
from dados import carregar_noticias

st.title("📰 Notícias Extraídas via Web Scraping")
df = carregar_noticias()

if df.empty:
    st.warning("Nenhum dado em Data/Processed. Execute antes o 'coletor_noticias.py'.")
    st.stop()

fontes = st.multiselect("Filtrar por fonte", sorted(df["fonte"].dropna().unique()))
if fontes:
    df = df[df["fonte"].isin(fontes)]

st.metric("Total de manchetes", len(df))
st.dataframe(df)