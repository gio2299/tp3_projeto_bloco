# EquidadeJá Brasil — TP3

Painel de equidade de gênero no mercado de trabalho brasileiro.
Projeto de Bloco: Inteligência Artificial Aplicada — Giovanna Silva.

## O que o projeto tem
- Aplicação Streamlit com múltiplas páginas (indicadores, notícias, nuvem de palavras, upload/download, API e sobre)
- API com FastAPI (consulta e envio de dados)
- Web scraping dinâmico com Selenium (texto completo das notícias)
- Corpus de dados preparado para uso com LLMs

## Como instalar
```bash
python -m venv .venv
.venv\Scripts\activate        # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Como rodar
**Aplicação (Streamlit):**
```bash
streamlit run app.py
```

**API (FastAPI)**, em outro terminal:
```bash
uvicorn api:app --port 8000
```
Documentação interativa: http://localhost:8000/docs

**Scraping com Selenium** (requer Google Chrome instalado):
```bash
python scraping_selenium.py
```

**Preparar o corpus para LLM:**
```bash
python preparar_corpus.py
```

## Rotas da API
| Método | Rota | Função |
|---|---|---|
| GET | `/` | Verifica se a API está no ar |
| GET | `/indicadores` | Lista indicadores (filtros `ano_inicio`, `ano_fim`) |
| GET | `/noticias` | Lista notícias (filtros `fonte`, `limite`) |
| POST | `/noticias` | Cadastra uma notícia |
| GET | `/estatisticas` | Resumo dos dados |

## Documentação
Veja a pasta `docs/` (Project Charter e Data Summary Report).

## Uso de IA
Ferramentas de IA generativa (Claude, Anthropic) foram usadas como apoio no código e na documentação, com revisão da autora.