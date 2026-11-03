import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from dados import ARQ_NOTICIAS, carregar_noticias, carregar_indicadores

app = FastAPI(
    title="EquidadeJá Brasil API",
    description="Consulta e envio de dados sobre equidade de gênero no trabalho.",
    version="1.0.0",
)


class Noticia(BaseModel):
    titulo: str
    fonte: str
    data: str
    link: str


def para_json(df: pd.DataFrame):
    """Troca valores vazios (NaN) por None, senão o JSON quebra."""
    return df.astype(object).where(df.notna(), None).to_dict(orient="records")


@app.get("/", tags=["Geral"])
def status():
    """Verifica se a API está no ar."""
    return {"status": "ok", "projeto": "EquidadeJá Brasil"}


@app.get("/indicadores", tags=["Indicadores"])
def listar_indicadores(
    ano_inicio: Optional[int] = Query(None, description="Filtra a partir deste ano"),
    ano_fim: Optional[int] = Query(None, description="Filtra até este ano"),
):
    """Retorna os indicadores de gênero, com filtro opcional por período."""
    df = carregar_indicadores()
    if ano_inicio is not None:
        df = df[df["ano"] >= ano_inicio]
    if ano_fim is not None:
        df = df[df["ano"] <= ano_fim]
    return para_json(df)


@app.get("/noticias", tags=["Notícias"])
def listar_noticias(
    fonte: Optional[str] = Query(None, description="Filtra por fonte (busca parcial)"),
    limite: int = Query(20, ge=1, le=100, description="Máximo de resultados"),
):
    """Retorna as notícias coletadas, com filtro opcional por fonte."""
    df = carregar_noticias()
    if fonte:
        df = df[df["fonte"].str.contains(fonte, case=False, na=False)]
    return para_json(df.head(limite))


@app.post("/noticias", status_code=201, tags=["Notícias"])
def adicionar_noticia(noticia: Noticia):
    """Adiciona uma nova notícia ao arquivo de dados."""
    df = carregar_noticias()
    if noticia.link in df["link"].values:
        raise HTTPException(status_code=409, detail="Notícia já cadastrada.")
    novo = pd.DataFrame([noticia.model_dump()])
    pd.concat([df, novo], ignore_index=True).to_csv(ARQ_NOTICIAS, index=False)
    return {"mensagem": "Notícia adicionada com sucesso", "total": len(df) + 1}


@app.get("/estatisticas", tags=["Geral"])
def estatisticas():
    """Resumo: total de notícias e média de cada indicador."""
    ind = carregar_indicadores()
    return {
        "total_noticias": len(carregar_noticias()),
        "media_por_indicador": ind.groupby("indicador")["valor"].mean().round(2).to_dict(),
    }