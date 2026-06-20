# Base de Conhecimento

## Dados Utilizados

O Agent Skopos utiliza uma base de conhecimento local e estruturada, focada inteiramente em objetivos de vida e comportamento financeiro real, substituindo os arquivos genéricos do repositório base pelos seguintes datasets personalizados:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_financeiro.csv` | CSV | Define o perfil de planejamento do usuário, sua renda mensal, capacidade de poupança esperada e a lista detalhada de metas ativas (com valores, prazos e prioridades).|
| `metas_usuario.json` | JSON | Registra o comportamento real de consumo do usuário (entradas e saídas recentes) para monitorar desvios orçamentários |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Sim, os dados foram totalmente reestruturados e limpos. O repositório original trazia arquivos voltados para investimentos genéricos (perfil_investidor.json) e transações bancárias tradicionais (transacoes.csv).

Para o Agent Skopos, as seguintes modificações profundas foram feitas no VS Code:

1. Renomeação Estrutural: Alteração física dos nomes dos arquivos na pasta data/ para refletir o escopo de planejamento de metas (metas_usuario.json e historico_financeiro.csv).

2. Nova Lógica no JSON: O arquivo JSON foi expandido para conter um array de objetos chamado metas_ativas, onde cada meta possui variáveis como valor_alvo, valor_atual, prazo_meses e prioridade.

3. Alinhamento Orçamentário no CSV: Os dados mockados do CSV de transações foram recalculados para simular um cenário real de gastos supérfluos (como excesso em categorias de Lazer e Delivery), permitindo que a IA aplique sua lógica preditiva de cortes.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os dados são carregados na inicialização da aplicação através do script principal src/app.py. O arquivo historico_financeiro.csv é lido e estruturado utilizando a biblioteca Pandas, enquanto o arquivo metas_usuario.json é interpretado nativamente pela biblioteca json do Python. Ambos os conteúdos são consolidados em memória logo na abertura da sessão do Streamlit.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são carregados na inicialização da aplicação através do script principal src/app.py. O arquivo historico_financeiro.csv é lido e estruturado utilizando a biblioteca Pandas, enquanto o arquivo metas_usuario.json é interpretado nativamente pela biblioteca json do Python. Ambos os conteúdos são consolidados em memória logo na abertura da sessão do Streamlit.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Usuário e Metas (metas_usuario.json):
{
  "usuario": "Camila Silva",
  "perfil_planejamento": "Focado",
  "renda_mensal": 5000.0,
  "capacidade_poupanca_mes": 1000.0,
  "metas_ativas": [
    {
      "id": 1,
      "descricao": "Reserva de Emergência",
      "valor_alvo": 12000.0,
      "valor_atual": 4500.0,
      "prazo_meses": 12,
      "prioridade": "Alta"
    },
    {
      "id": 2,
      "descricao": "Notebook Novo para Estudos",
      "valor_alvo": 4000.0,
      "valor_atual": 1500.0,
      "prazo_meses": 5,
      "prioridade": "Média"
    }
  ]
}

Histórico Recente de Transações (historico_financeiro.csv):
      data   categoria                 descricao   valor    tipo
2026-06-01     Receita           Salário Mensal  5000.00 credito
2026-06-02   Habitação     Aluguel e Condomínio  1800.00  debito
2026-06-05 Alimentação              Supermercado   650.00  debito
2026-06-12 Alimentação    Delivery Fim de Semana   150.00  debito
2026-06-10       Lazer           Cinema e Jantar   180.00  debito
...
```
