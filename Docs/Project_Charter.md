# Project Charter — EquidadeJá Brasil

> **Versão TP3 (revisada em 02/11/2026).** As seções alteradas ou novas em relação à versão do TP1/TP2 estão marcadas com **[TP3]**.

## 1. Nome do Projeto
**EquidadeJá Brasil** — Painel de monitoramento da equidade de gênero no mercado de trabalho brasileiro.

## 2. Contexto e Problema de Negócio
Apesar de avanços legais e de discursos corporativos sobre diversidade, mulheres no Brasil ainda enfrentam desigualdades relevantes no mercado de trabalho: menor participação na força de trabalho, sub-representação em cargos de liderança e diferenças salariais persistentes em relação aos homens. Empresas com metas ESG, áreas de RH e formuladores de políticas públicas frequentemente têm dificuldade em acompanhar, de forma acessível e contextualizada, a evolução desses indicadores — e em traduzir números frios em ações concretas.

**Problema de negócio:** Falta de uma ferramenta que combine (i) indicadores oficiais e atualizados sobre participação e representatividade de gênero no mercado de trabalho, (ii) contexto qualitativo do noticiário sobre o tema, e (iii) interpretação acionável desses dados — hoje dispersos e sem conexão entre si.

### 2.1 Reavaliação do problema de negócio **[TP3]**
Com as novas ferramentas incorporadas nesta etapa (FastAPI, Selenium e Streamlit multipágina), o problema de negócio permanece o mesmo, mas a forma de resolvê-lo ficou mais robusta, e as metas foram ajustadas:

- **Integração com outros sistemas:** com a API FastAPI, os dados deixam de ficar presos ao dashboard. Um sistema de RH ou de relatórios ESG pode consultar os indicadores e as notícias por requisições HTTP (GET) e enviar novas notícias (POST), sem depender da interface.
- **Contexto qualitativo mais profundo:** o RSS do Google News fornece apenas título, fonte, data e link. Com o Selenium, o texto completo das matérias passa a ser coletado, permitindo análises mais ricas (resumo, sentimento, perguntas e respostas) do que seria possível só com manchetes.
- **Navegação mais clara:** o painel deixa de ser uma página única com abas e passa a ter várias páginas com menu lateral, o que facilita o uso por públicos não técnicos.
- **Preparação para IA:** os dados coletados foram organizados em um corpus único, pronto para uso com LLMs na próxima etapa.

## 3. Objetivos do Projeto
- Consolidar indicadores públicos sobre participação de mulheres na força de trabalho e representatividade em posições de liderança/decisão.
- Coletar, via web scraping, notícias recentes sobre equidade de gênero no mercado de trabalho brasileiro, para dar contexto qualitativo aos números.
- **[TP3]** Expor os dados por meio de uma API (FastAPI), permitindo consulta e envio de informações por outros sistemas.
- **[TP3]** Extrair o texto completo das notícias por meio de scraping dinâmico (Selenium), ampliando o contexto qualitativo.
- Utilizar um LLM (via engenharia de prompts) para gerar automaticamente resumos executivos e insights acionáveis, cruzando dados quantitativos com o noticiário coletado. **[TP3]** Esta funcionalidade foi reposicionada para a próxima etapa, e nesta fase os dados foram preparados para ela.
- Apresentar tudo em um dashboard interativo em Streamlit, acessível para públicos não técnicos. **[TP3]** Agora com múltiplas páginas e menu de navegação.

## 4. Metas e Indicadores de Sucesso (KPIs)
| Indicador | Meta para o projeto | Status |
|---|---|---|
| Cobertura de dados históricos | Série de pelo menos 15 anos para os indicadores de participação no mercado de trabalho | Parcial: a amostra local atual cobre 2015–2022 (8 anos) |
| Atualização dos dados | Coleta automatizada via API (sem necessidade de atualização manual) | Em andamento |
| Volume de contexto qualitativo | Ao menos 10 manchetes recentes coletadas por execução do scraper | Atingido (15 manchetes) |
| **[TP3]** Texto completo das notícias | Extrair o texto de ao menos 60% das notícias via Selenium | Atingido (14 de 15 notícias, 93%) |
| **[TP3]** API de dados | Ao menos 2 rotas (GET e POST) documentadas e funcionais | Atingido (5 rotas: 4 GET e 1 POST) |
| **[TP3]** Navegação | Aplicação com menu e ao menos 5 páginas | Atingido (página inicial + 6 páginas) |
| Qualidade dos insights gerados | Resumos do LLM revisados e validados manualmente quanto à fidelidade aos dados (sem "alucinações") | Próxima etapa |
| Usabilidade | Dashboard navegável por um usuário de RH/ESG sem necessidade de treinamento técnico | Em validação |
| Adoção | Validação do protótipo por ao menos 1 usuário-teste da área de RH ou D&I | Próxima etapa |

## 5. ODS (Objetivos de Desenvolvimento Sustentável) Atendidos
- **ODS 5 — Igualdade de Gênero:** o projeto monitora diretamente indicadores de participação econômica e representatividade de mulheres, centrais para acompanhar o progresso desse ODS no Brasil.
- **ODS 8 — Trabalho Decente e Crescimento Econômico:** ao evidenciar disparidades na força de trabalho, o projeto contribui para o acompanhamento de metas relacionadas a emprego pleno e produtivo, e trabalho decente para todas as pessoas, sem distinção de gênero.

**Justificativa:** Existem indicadores oficiais e mensuráveis para ambos os ODS (ex: taxa de participação feminina na força de trabalho, % de assentos ocupados por mulheres em posições de decisão), disponíveis em bases abertas como o Banco Mundial. Além disso, o tema é um pilar central da dimensão **Social (S)** do ESG, com forte demanda de empresas por instrumentos de acompanhamento.

## 6. Público-Alvo
- Áreas de RH, Diversidade & Inclusão (D&I) e ESG em empresas.
- Formuladores de políticas públicas voltadas à equidade de gênero.
- ONGs e movimentos de defesa dos direitos das mulheres.
- Pesquisadores, jornalistas de dados e estudantes interessados no tema.
- **[TP3]** Desenvolvedores e sistemas internos de empresas, que passam a poder consumir os dados pela API.

## 7. Escopo
**Incluído neste projeto:**
- Definição do problema, metas e ODS.
- Estrutura do projeto em TDSP/CRISP-DM.
- Coleta de dados via API (Banco Mundial — indicadores de gênero no mercado de trabalho).
- Coleta de dados via Web Scraping (manchetes de notícias via feed RSS público).
- **[TP3]** Scraping dinâmico com Selenium para extração do texto completo das matérias.
- **[TP3]** API REST com FastAPI (consulta e envio de dados).
- **[TP3]** Dashboard Streamlit com múltiplas páginas e menu de navegação.
- **[TP3]** Preparação dos dados (corpus) para uso com LLMs.
- Geração de insights com LLM via engenharia de prompts (API da Anthropic) — a ser integrada na próxima etapa.

**Fora do escopo (possíveis evoluções futuras):**
- Deploy em ambiente de produção/nuvem.
- Modelos preditivos (ex: previsão de evolução dos indicadores).
- Análise de sentimento aprofundada do noticiário com NLP dedicado (será abordada de forma introdutória com LLM na próxima etapa).

## 8. Stakeholders
| Papel | Responsável | Interesse no projeto |
|---|---|---|
| Product Owner / Autor do projeto | Giovanna Silva | Entregar solução funcional e alinhada à disciplina |
| Professor / Avaliador | Renan Silva Santos | Avaliar aderência aos métodos TDSP/CRISP-DM e qualidade técnica |
| Usuário final (persona) | Analista de RH / ESG / D&I | Usar o dashboard para embasar decisões e relatórios |
| **[TP3]** Sistemas consumidores | Sistemas internos de RH/ESG | Consultar os dados pela API FastAPI |
| Fonte de dados quantitativos | Banco Mundial (World Bank Open Data API) | Fornecer indicadores confiáveis e atualizados |
| Fonte de dados qualitativos | Google News (feed RSS público) e sites de notícias | Fornecer contexto noticioso recente sobre o tema |
| Provedor de LLM | Anthropic (API Claude) | Gerar insights textuais a partir dos dados coletados |

## 9. Premissas e Riscos
**Premissas:**
- As APIs e feeds públicos escolhidos permanecerão disponíveis e gratuitos.
- O usuário terá uma chave de API da Anthropic válida para gerar os insights (etapa de LLM); sem ela, o app funciona normalmente nas demais páginas.
- **[TP3]** Para usar a página "API" do dashboard, o servidor FastAPI precisa estar em execução localmente (`uvicorn api:app --port 8000`).
- **[TP3]** O Google Chrome precisa estar instalado para executar o scraping com Selenium.

**Riscos:**
- Instabilidade da API do Banco Mundial ou do feed de notícias (mitigação: cache local + dados de amostra como fallback).
- Insights gerados por LLM podem conter interpretações imprecisas (mitigação: prompt restringe o modelo a usar apenas os dados fornecidos, e o texto é sempre apresentado como sugestão, não como fato definitivo).
- Estrutura de páginas de notícias pode mudar (mitigação: uso de feed RSS, mais estável que scraping de HTML de páginas de notícia).
- **[TP3]** Sites de notícias podem bloquear robôs ou ter paywall, o que impede a extração do texto completo (mitigação: registrar a taxa de sucesso e manter a manchete como fallback).
- **[TP3]** O Google News pode alterar o formato dos links de redirecionamento do RSS, quebrando o scraping dinâmico (mitigação: manter o script simples e revisar periodicamente).
- **[TP3]** A página da API depende do servidor local estar ligado (mitigação: mensagem clara de erro e instruções de inicialização na própria página).
- **[TP3]** Direitos autorais sobre o texto completo das matérias (mitigação: uso restrito a fins acadêmicos, sem republicação do conteúdo no painel).

## 10. Cronograma Macro (alinhado às fases TDSP)
| Fase TDSP | Entrega | Status |
|---|---|---|
| Business Understanding | Project Charter, definição de ODS e público-alvo | ✅ Concluído (revisado no TP3) |
| Data Acquisition & Understanding | Data Summary Report, coleta via API e Web Scraping | ✅ Concluído (ampliado no TP3 com Selenium) |
| **[TP3]** Aplicação e API | Streamlit multipágina + API FastAPI | ✅ Concluído no TP3 |
| **[TP3]** Preparação para LLM | Corpus organizado em `Data/LLM/corpus_llm.csv` | ✅ Concluído no TP3 |
| Modeling | Integração de LLM: resumo, sentimento e perguntas e respostas | 🔲 Próxima etapa |
| Deployment | Dashboard final integrando todas as fontes e a IA | 🔲 Próxima etapa |
| Customer Acceptance | Validação com usuário-teste, ajustes finais | 🔲 Próxima etapa |
