import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from dados import carregar_corpus

STOPWORDS_PT = set("""
a o as os um uma uns umas de da do das dos em na no nas nos para por com sem sob sobre
entre até e ou mas que se não mais menos como já só também ao aos à às pelo pela pelos
pelas seu sua seus suas é são foi ser ter há br www com pouco uma
""".split())

st.title("☁️ Nuvem de Palavras dos Conteúdos Raspados")
texto = carregar_corpus()

if not texto:
    st.warning("Arquivo 'corpus_noticias.txt' não encontrado em Data/Processed.")
    st.stop()

wc = WordCloud(width=900, height=450, background_color="white",
               stopwords=STOPWORDS_PT, collocations=False).generate(texto)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)