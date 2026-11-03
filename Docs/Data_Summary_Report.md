# Data Summary Report — EquidadeJá Brasil

> **Versão TP3 (revisada em 02/11/2026).** As seções alteradas ou novas em relação à versão anterior estão marcadas com **[TP3]**.

## 1. Objetivo deste documento
Relacionar todas as fontes de dados utilizadas no projeto EquidadeJá Brasil, indicando tipo de dado, formato de acesso e finalidade de uso — cobrindo as frentes de coleta do projeto: **API**, **Web Scraping (estático e dinâmico)** e **entrada para o LLM**. **[TP3]** Este documento também descreve os arquivos gerados e como os dados são servidos pela API do projeto.

## 2. Fontes de Dados

### 2.1 World Bank Open Data API (dados quantitativos — API)
- **URL:** https://api.worldbank.org/v2/
- **Tipo de dado:** Série temporal numérica por país/ano.
- **Formato de acesso:** API REST pública, sem chave/autenticação, retorno em JSON.
- **Indicadores utilizados:**
  - `SL.TLF.CACT.FE.ZS` — Taxa de participação na força de trabalho, mulheres (% da população feminina 15+).
  - `SL.TLF.CACT.MA.ZS` — Taxa de participação na força de trabalho, homens (% da população masculina 15+).
  - `SG.GEN.PARL.ZS` — Proporção de assentos ocupados por mulheres em parlamentos nacionais (%), usado como proxy de representatividade em posições de decisão.
- **Objetivo de uso:** Base quantitativa principal do dashboard — evolução histórica da diferença de participação de gênero no mercado de trabalho e da representatividade em posições de decisão no Brasil.
- **Observações:** dados podem ter defasagem de 1–2 anos; tratados com cache local (`Sample Data/`) como fallback.
- **[TP3] Situação atual:** o painel multipágina lê a amostra local `Sample Data/amostra_indicadores_genero.csv`, que cobre os anos de 2015 a 2022 para os indicadores de participação feminina e masculina na força de trabalho. Esses dados também são servidos pela rota `GET /indicadores` da API do projeto.

### 2.2 Google News RSS Feed (dados qualitativos — Web Scraping estático)
- **URL base:** `https://news.google.com/rss/search?q={termo}&hl=pt-BR&gl=BR&ceid=BR:pt-419`
- **Tipo de dado:** Texto (título, link, data de publicação, fonte) de notícias recentes.
- **Formato de acesso:** Feed RSS público (XML), consumido via requisição HTTP e parsing de XML (Beautiful Soup) — caracteriza **Web Scraping** de uma fonte pública estruturada.
- **Termos de busca utilizados:** "equidade de gênero trabalho Brasil", "diferença salarial mulheres homens Brasil", "mulheres liderança empresas Brasil".
- **Objetivo de uso:** Fornecer contexto qualitativo e atual (eventos, políticas, movimentos recentes) para complementar os indicadores numéricos, e servir de insumo para a geração de insights via LLM.
- **Observações:** o feed fornece apenas título, fonte, data e link. Os links do RSS são redirecionamentos do Google News e não levam diretamente ao texto da matéria.
- **[TP3] Volume atual:** 15 manchetes coletadas.

### 2.3 Páginas das matérias via Selenium (dados qualitativos — Web Scraping dinâmico) **[TP3 — fonte nova]**
- **URL:** links das 15 manchetes do feed RSS (`news.google.com/rss/articles/...`), que redirecionam para os sites originais dos veículos.
- **Tipo de dado:** Texto completo das matérias (parágrafos) e URL final do artigo.
- **Formato de acesso:** páginas HTML carregadas em um navegador Chrome automatizado (Selenium, modo headless). O redirecionamento do Google News é feito por JavaScript, o que torna o Beautiful Soup insuficiente: é preciso um navegador real que execute o script e aguarde o carregamento da página de destino.
- **Script:** `scraping_selenium.py`.
- **Arquivo gerado:** `Data/Processed/noticias_completas.csv`.
- **Objetivo de uso:** obter o conteúdo integral das matérias para análises mais profundas com LLMs na próxima etapa (resumo, classificação de sentimento, perguntas e respostas).
- **Resultado da coleta:** texto extraído de 15 das 15 notícias (100%).
- **Limitações:** alguns sites podem bloquear robôs, exigir assinatura (paywall) ou alterar o HTML; o script extrai apenas parágrafos com mais de 60 caracteres e, por isso, pode omitir trechos curtos. O resultado depende do estado dos sites no momento da execução.

### 2.4 API da Anthropic (Claude) — geração de insights via LLM
- **Tipo de dado:** Texto gerado (resumo executivo / insight) a partir de um prompt estruturado.
- **Formato de acesso:** API REST (`api.anthropic.com/v1/messages`), requer chave de API própria do usuário.
- **Entrada do prompt (dados que alimentam o LLM):**
  - Resumo estatístico dos indicadores do Banco Mundial (últimos valores e tendência).
  - Lista de manchetes coletadas via Web Scraping (título + fonte + data).
  - **[TP3]** Texto completo das matérias, obtido via Selenium.
- **Objetivo de uso:** Gerar, em linguagem natural, um resumo executivo e um insight acionável para o público de RH/ESG, cruzando dados quantitativos e qualitativos — sem que o modelo invente números não presentes nos dados fornecidos (restrição aplicada via engenharia de prompt).
- **Observações:** funcionalidade opcional — caso o usuário não tenha uma chave de API configurada, o dashboard continua funcional nas demais páginas.
- **[TP3] Situação atual:** nesta etapa os dados foram **preparados** para o uso com LLM (ver seção 3). A integração do modelo ao painel será feita na próxima etapa.

## 3. Arquivos de dados do projeto **[TP3]**

| Arquivo | Origem | Colunas | Uso |
|---|---|---|---|
| `Sample Data/amostra_indicadores_genero.csv` | World Bank (amostra local) | `ano`, `valor`, `indicador` | Página "Indicadores", rota `/indicadores` |
| `Data/Processed/noticias_equidade.csv` | Google News RSS | `titulo`, `fonte`, `data`, `link` | Página "Notícias", rotas `/noticias` |
| `Data/Processed/corpus_noticias.txt` | Texto das manchetes | texto corrido | Página "Nuvem de Palavras" |
| `Data/Processed/noticias_completas.csv` | Selenium | colunas de `noticias_equidade.csv` + `url_final`, `texto`, `tamanho_texto` | Insumo para o corpus de LLM |
| `Data/LLM/corpus_llm.csv` | Notícias + indicadores | `tipo`, `titulo`, `fonte`, `data`, `conteudo` | Corpus único para as tarefas com LLM |

**Sobre o corpus de LLM:** cada notícia vira um documento (`título + texto completo`), e cada valor de indicador é convertido em uma frase em linguagem natural (ex.: "Em 2019, o indicador 'Taxa de participação na força de trabalho - Mulheres (%)' foi de 55.1."), pois modelos de linguagem interpretam texto melhor do que tabelas.

## 4. API do projeto (FastAPI) **[TP3]**
Os dados acima são servidos por uma API REST (`api.py`), executada com `uvicorn api:app --port 8000`. A documentação interativa é gerada automaticamente em `http://localhost:8000/docs`.

| Método | Rota | Função | Parâmetros |
|---|---|---|---|
| GET | `/` | Verifica se a API está no ar | nenhum |
| GET | `/indicadores` | Lista os indicadores | `ano_inicio`, `ano_fim` (opcionais) |
| GET | `/noticias` | Lista as notícias coletadas | `fonte`, `limite` (opcionais) |
| POST | `/noticias` | Cadastra uma nova notícia | JSON: `titulo`, `fonte`, `data`, `link` |
| GET | `/estatisticas` | Total de notícias e média por indicador | nenhum |

## 5. Resumo em Tabela

| Fonte | Tipo de Dado | Formato | Método de Coleta | Uso no Projeto | Status |
|---|---|---|---|---|---|
| World Bank API | Numérico, série temporal | JSON via API REST | API | Indicadores quantitativos do dashboard e da API | ✅ Integrado (amostra local 2015–2022) |
| Google News RSS | Texto (manchetes) | XML (RSS) | Web Scraping estático | Contexto qualitativo + insumo para o LLM | ✅ Integrado (15 manchetes) |
| **[TP3]** Páginas das matérias | Texto completo | HTML dinâmico | Web Scraping com Selenium | Insumo para resumo, sentimento e Q&A | ✅ Integrado (15/15 com texto) |
| Anthropic API (Claude) | Texto gerado | JSON via API REST | Geração via LLM / prompt engineering | Insight executivo combinando dados + notícias | 🔲 Dados preparados; integração na próxima etapa |

## 6. Qualidade e limitações dos dados **[TP3]**
- **Cobertura temporal:** a amostra de indicadores cobre 2015–2022, abaixo da meta de 15 anos definida no Project Charter. A ampliação da série é uma melhoria pendente.
- **Volume de notícias:** 15 manchetes, volume pequeno e suficiente para a demonstração, mas limitado para análises estatísticas.
- **Viés de seleção:** as notícias dependem dos termos de busca e do ranking do Google News, o que pode privilegiar certos veículos.
- **Datas variadas:** o feed traz matérias de datas bem distintas (de 2022 a 2026), de modo que nem todas são "recentes".
- **Texto extraído:** o texto vem de parágrafos da página e pode incluir trechos de menus, chamadas ou publicidade; a limpeza é feita em `preparar_corpus.py` (remoção de espaços extras).

## 7. Considerações Éticas e de Direitos Autorais
- O feed RSS é uma interface pública desenhada para consumo/syndication e é preferido ao scraping direto de HTML sempre que possível.
- **[TP3]** O texto completo das matérias coletado com Selenium é usado apenas para fins acadêmicos e de análise. O painel exibe títulos, fontes e links, e direciona o usuário à fonte original; o conteúdo integral não é republicado.
- **[TP3]** O scraping usa pausas entre as requisições (1 segundo) para não sobrecarregar os sites.
- Os insights gerados por LLM serão apresentados como **sugestões geradas por IA**, não como fatos definitivos, e o prompt instruirá o modelo a não inventar dados fora do que foi fornecido. Modelos de linguagem podem ter vieses e imprecisões, e a validação das informações é responsabilidade da autora.

## 8. Próximos Passos
- Integrar o LLM ao painel: resumo das matérias, classificação de sentimento e perguntas e respostas sobre os dados.
- Ampliar a série histórica dos indicadores (meta de 15 anos) e conectar a coleta diretamente à API do Banco Mundial.
- Avaliar inclusão de dados do IBGE (PNAD Contínua) para detalhamento nacional/regional, como fonte complementar.
- Coletar feedback de um usuário-teste da área de RH/D&I sobre a utilidade do painel e dos insights.
- Validar periodicamente se os termos de busca e o scraping continuam retornando resultados relevantes.
