# 🎯 Agent Skopos — Planejador Estratégico de Metas com IA Generativa

## Contexto e Visão Geral

O **Agent Skopos** é um agente financeiro inteligente, proativo e consultivo, desenvolvido para transformar dados financeiros estáticos em planejamento preditivo de metas de vida. 

Enquanto a maioria das aplicações do mercado atua de forma reativa (mostrando apenas o histórico de gastos passados), o Skopos cruza o comportamento de consumo atual do usuário com seus objetivos de curto, médio e longo prazo. Ele atua como um mentor financeiro estratégico que valida prazos, calcula viabilidade de depósitos e propõe soluções realistas de redirecionamento orçamentário.

---

## 🛠️ Tecnologias e Infraestrutura Utilizadas

A solução foi construída utilizando práticas modernas de engenharia de IA e desenvolvimento de software:

*   **Interface Gráfica:** [Streamlit](https://streamlit.io/) para a renderização do dashboard preditivo e chat interativo em tempo real.
*   **Processamento e IA:** Nova biblioteca unificada **`google-genai`** integrada aos modelos de última geração da família **Gemini**.
*   **Análise de Dados:** [Pandas](https://pandas.pydata.org/) para ingestão, manipulação e cruzamento de bases de dados estruturadas.
*   **Segurança de Escopo:** [Python-dotenv](https://pypi.org/project/python-dotenv/) para isolamento estrito de credenciais sensíveis e chaves de API.

---

## 📁 Estrutura do Repositório

```text
📁 agent-skopos-genia/
│
├── 📄 README.md                      # Instruções gerais e guia de execução
├── 📄 .env                           # Variáveis de ambiente protegidas (API_KEY)
│
├── 📁 data/                          # Base de dados estruturada (Ground Truth)
│   ├── historico_financeiro.csv      # Histórico de transações da usuária (CSV)
│   └── metas_usuario.json            # Metas ativas, prazos e prioridades (JSON)
│
├── 📁 docs/                          # Documentação detalhada do projeto
│   ├── 01-documentacao-agente.md     # Caso de uso e arquitetura preditiva
│   ├── 02-base-conhecimento.md       # Estratégia de modelagem de dados
│   ├── 03-prompts.md                 # Engenharia de System Prompt e Guardrails
│   ├── 04-metricas.md                # Framework de avaliação e cenários de teste
│   └── 05-pitch.md                   # Roteiro do pitch gravado de 3 minutos
│
└── 📁 src/                           # Código-fonte da aplicação funcional
    ├── app.py                        # Ponto de entrada da interface Streamlit
    ├── agente.py                     # Lógica de integração com o cliente Gemini
    ├── config.py                     # Inicializações e tratamento de variáveis
    └── requirements.txt              # Dependências do ecossistema Python
```
---

## ⚙ Como Rodar o Projeto Localmente

1. Pré-requisitos
Certifique-se de ter o Python 3.10 ou superior instalado na sua máquina.

2. Clonar o Repositório e Acessar a Pasta
```
 git clone [https://github.com/NayaraFreitas/agent-skopos-genia.git](https://github.com/NayaraFreitas/agent-skopos-genia.git)
cd agent-skopos-genia
```

3. Criar e Ativar o Ambiente Virtual (.venv)
No Windows (PowerShell):
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```
4. Instalar as Dependências Atualizadas
Instale os pacotes necessários que estão mapeados dentro da pasta src/:
```
pip install -r src/requirements.txt
```

5. Configurar a Chave de API (.env)
Crie um arquivo chamado .env na raiz do projeto (fora da pasta src/). Adicione a sua chave obtida no Google AI Studio seguindo o formato rigoroso de sanitização (sem aspas e sem espaços colados no operador =):

```
GEMINI_API_KEY=AIzaSyA1234ExemploDeChaveOriginalDoGoogleAIStudio
```
6. Executar a Aplicação Streamlit
Com o ambiente ativado e a chave configurada, rode o comando especificando o caminho do script principal:

```
streamlit run src/app.py
```