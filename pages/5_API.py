import requests
import pandas as pd
import streamlit as st

API = "http://localhost:8000"

st.title("🔌 Dados via API (FastAPI)")
st.caption("Esta página consome a API local. Inicie com: uvicorn api:app --port 8000")

try:
    st.success(f"API online: {requests.get(API, timeout=3).json()}")
except requests.exceptions.RequestException:
    st.error("API fora do ar. Inicie o servidor FastAPI em outro terminal.")
    st.stop()

st.subheader("GET /noticias")
fonte = st.text_input("Filtrar por fonte (opcional)")
limite = st.slider("Limite", 1, 50, 10)
resp = requests.get(f"{API}/noticias", params={"fonte": fonte or None, "limite": limite})
st.dataframe(pd.DataFrame(resp.json()))

st.subheader("GET /estatisticas")
st.json(requests.get(f"{API}/estatisticas").json())

st.subheader("POST /noticias: adicionar notícia")
with st.form("nova_noticia"):
    titulo = st.text_input("Título")
    fonte_n = st.text_input("Fonte")
    data = st.text_input("Data")
    link = st.text_input("Link")
    if st.form_submit_button("Enviar"):
        r = requests.post(f"{API}/noticias",
                          json={"titulo": titulo, "fonte": fonte_n, "data": data, "link": link})
        if r.status_code == 201:
            st.success(r.json())
        else:
            st.error(r.json())