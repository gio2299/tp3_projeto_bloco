import streamlit as st
from dados import carregar_noticias, carregar_indicadores

st.set_page_config(page_title="EquidadeJá Brasil", page_icon="⚖️", layout="wide")

st.title("⚖️ EquidadeJá Brasil")
st.subheader("Painel de Equidade de Gênero no Mercado de Trabalho Brasileiro")

st.markdown("Use o **menu lateral** para navegar entre as seções do painel.")

col1, col2, col3 = st.columns(3)
col1.metric("Manchetes coletadas", len(carregar_noticias()))
col2.metric("Indicadores disponíveis", carregar_indicadores()["indicador"].nunique())
col3.metric("ODS atendidos", "5 e 8")

st.markdown("""
### Seções
- **Indicadores**: dados oficiais de participação no mercado de trabalho
- **Notícias**: manchetes coletadas por web scraping
- **Nuvem de Palavras**: termos mais frequentes nas notícias
- **Upload & Download**: envie e baixe arquivos
- **API**: dados servidos pela API FastAPI
- **Sobre**: ODS e metodologia
""")