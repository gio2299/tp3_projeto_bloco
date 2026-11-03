import streamlit as st
import plotly.express as px
from dados import carregar_indicadores

st.title("📈 Indicadores Oficiais de Gênero")
st.caption("Fonte: World Bank Open Data / amostra local")

df = carregar_indicadores()
if df.empty:
    st.warning("Nenhum indicador encontrado em 'Sample Data'.")
    st.stop()

escolhidos = st.multiselect("Indicadores", sorted(df["indicador"].unique()),
                            default=sorted(df["indicador"].unique()))
filtrado = df[df["indicador"].isin(escolhidos)]

st.subheader("Tabela de Indicadores")
st.dataframe(filtrado)

st.subheader("Evolução Temporal")
fig = px.line(filtrado, x="ano", y="valor", color="indicador", markers=True)
fig.update_layout(legend=dict(orientation="h", y=-0.3))
st.plotly_chart(fig)