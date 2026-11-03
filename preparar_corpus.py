import pandas as pd
from dados import ROOT, ARQ_COMPLETAS, carregar_noticias, carregar_indicadores

if ARQ_COMPLETAS.exists():
    noticias = pd.read_csv(ARQ_COMPLETAS)
else:
    noticias = carregar_noticias()
    noticias["texto"] = ""
    noticias["url_final"] = noticias["link"]

noticias["texto"] = (noticias["texto"].fillna("")
                     .str.replace(r"\s+", " ", regex=True).str.strip())
docs = pd.DataFrame({
    "tipo": "noticia",
    "titulo": noticias["titulo"],
    "fonte": noticias["fonte"],
    "data": noticias["data"],
    "conteudo": noticias["titulo"] + ". " + noticias["texto"],
})

# Indicadores viram frases (LLMs entendem texto melhor que tabela)
ind = carregar_indicadores()
frases = ind.apply(
    lambda r: f"Em {int(r['ano'])}, o indicador '{r['indicador']}' foi de {r['valor']}.", axis=1
)
ind_docs = pd.DataFrame({
    "tipo": "indicador", "titulo": "Indicador", "fonte": "World Bank / amostra local",
    "data": ind["ano"], "conteudo": frases,
})

saida = ROOT / "Data" / "LLM"
saida.mkdir(parents=True, exist_ok=True)
pd.concat([docs, ind_docs], ignore_index=True).to_csv(saida / "corpus_llm.csv", index=False)
print("Corpus salvo em", saida / "corpus_llm.csv")