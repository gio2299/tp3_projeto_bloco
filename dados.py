from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
ARQ_NOTICIAS = ROOT / "Data" / "Processed" / "noticias_equidade.csv"
ARQ_CORPUS = ROOT / "Data" / "Processed" / "corpus_noticias.txt"
ARQ_COMPLETAS = ROOT / "Data" / "Processed" / "noticias_completas.csv"
ARQ_INDICADORES = ROOT / "Sample Data" / "amostra_indicadores_genero.csv"


def carregar_noticias() -> pd.DataFrame:
    if ARQ_NOTICIAS.exists():
        return pd.read_csv(ARQ_NOTICIAS)
    return pd.DataFrame(columns=["titulo", "fonte", "data", "link"])


def carregar_corpus() -> str:
    if ARQ_CORPUS.exists():
        return ARQ_CORPUS.read_text(encoding="utf-8")
    return ""


def carregar_indicadores() -> pd.DataFrame:
    """Devolve sempre as colunas: ano, valor, indicador."""
    if ARQ_INDICADORES.exists():
        df = pd.read_csv(ARQ_INDICADORES)
    else:
        df = pd.DataFrame({
            "Ano": [2018, 2019, 2020, 2021, 2022],
            "Taxa de Participação Feminina (%)": [53.2, 54.1, 51.5, 52.8, 53.9],
            "Taxa de Participação Masculina (%)": [73.5, 73.8, 71.2, 72.0, 72.8],
        })
    df.columns = [c.strip().lower() if c.strip().lower() in ("ano", "valor", "indicador")
                  else c.strip() for c in df.columns]
    if {"ano", "valor", "indicador"}.issubset(df.columns):
        return df[["ano", "valor", "indicador"]]
    # formato "largo" (uma coluna por indicador) -> formato "longo"
    return df.melt(id_vars="ano", var_name="indicador", value_name="valor")