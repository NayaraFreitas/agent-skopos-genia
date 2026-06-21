# 📊 Avaliação e Métricas de Qualidade — Agent Skopos

Este documento estabelece a estratégia de validação, os cenários de teste e a matriz de métricas utilizada para garantir a confiabilidade, acurácia e resiliência do **Agent Skopos** como um planejador financeiro preditivo.

---

## 📐 Framework de Avaliação

O Agent Skopos é avaliado de forma contínua através de duas abordagens complementares:

1. **Testes Baseados em Cenários (Grounded Evaluation):** Validação estrita das respostas geradas contra a verdade contida nas bases de dados (`metas_usuario.json` e `historico_financeiro.csv`).
2. **Resiliência e Cobertura de API (Edge Cases):** Testes focados na estabilidade do agente diante de mudanças de escopo, atualizações de SDK/modelos e sanitização de variáveis de ambiente.

---

## 🎯 Matriz de Métricas de Qualidade

| Métrica | Dimensão Avaliada | Método de Validação | Meta Esperada |
| :--- | :--- | :--- | :--- |
| **Acurácia de Dados (Fidelidade)** | Capacidade de extrair e interpretar valores numéricos exatos dos arquivos JSON e CSV sem alucinações. | Comparação direta entre a resposta do agente e os valores reais das metas da usuária (Camila Silva). | **100% de precisão** em dados brutos. |
| **Alinhamento Estratégico (Prompt Guard)** | Aderência total às diretrizes do *System Prompt* (proatividade, tom mentor, respostas escaneáveis com bullet points). | Verificação visual da formatação e tom das respostas geradas no painel. | **100%** de respostas estruturadas. |
| **Abordagem Proativa (Regra de Ouro)** | Capacidade de identificar gargalos financeiros (ex: gastos excessivos no CSV) e propor caminhos alternativos. | Injeção de perguntas desafiadoras sobre o atingimento de metas difíceis. | **Compensação obrigatória** de diagnósticos negativos com soluções. |
| **Tratamento de Escopo e Exceções** | Recusa elegante de requisições fora do domínio de planejamento financeiro ou ausentes na base. | Testes com prompts de categorias não mapeadas ou informações inexistentes. | **Zero alucinações** ou vazamento de logs de erro para o usuário. |

---

## 🛠️ Cenários de Teste Estruturados (Benchmark)

Os cenários abaixo foram desenhados especificamente para o ecossistema de dados da usuária ativa **Camila Silva**:

### Teste 1: Consistência Cross-Data (Integração JSON + CSV)
* **Pergunta do Usuário:** "Vou conseguir cumprir a meta do Notebook Novo para Estudos no prazo atual?"
* **Contexto Esperado:** O agente deve ler a meta no JSON (Prazo: 5 meses, Valor: R$ 4000,00, Progresso: R$ 1500,00) e cruzar com a capacidade de poupança mensal (R$ 1000,00/mês). 
* **Cálculo da IA:** Faltam R$ 2500,00. Em 5 meses guardando R$ 1000,00, ela acumulará R$ 5000,00.
* **Resposta Esperada:** Confirmação positiva de que a meta é viável, trazendo os números exatos e demonstrando que haverá uma sobra financeira.
* **Resultado:** [ ] Aprovado  [ ] Reprovado

### Teste 2: Aplicação da Regra de Ouro (Diagnóstico + Solução)
* **Pergunta do Usuário:** "Consigo quitar minhas dívidas e fazer a Reserva de Emergência simultaneamente?"
* **Contexto Esperado:** Ao analisar o volume de metas de alta prioridade versus a renda, o agente detectará um gargalo de fluxo de caixa.
* **Resposta Esperada:** O agente deve apontar que o orçamento ficará severamente apertado (diagnóstico), mas **deve propor imediatamente** uma solução baseada no CSV (ex: sugerir cortes nas categorias supérfluas identificadas no histórico de transações).
* **Resultado:** [ ] Aprovado  [ ] Reprovado

### Teste 3: Tratamento de Input e Quebra de Escopo
* **Pergunta do Usuário:** "Qual é a previsão do tempo para hoje ou quem ganhou o último jogo?"
* **Contexto Esperado:** Testar a robustez dos guardrails do agente.
* **Resposta Esperada:** O agente deve recusar a resposta de forma educada, reforçando seu papel exclusivo como o Agent Skopos, especialista em inteligência financeira.
* **Resultado:** [ ] Aprovado  [ ] Reprovado

---

## 🚀 Engenharia de Resiliência e Logs de Erro

Durante o ciclo de desenvolvimento da solução, o agente passou por um processo rigoroso de refatoração para garantir estabilidade contra depreciações tecnológicas:

* **Sanitização do Ambiente (`.env`):** Implementação de travas de segurança no código (`.strip().replace()`) para mitigar erros de cabeçalho (`INTERNAL: Illegal header value`) causados por espaços ou aspas residuais na ingestão da `GEMINI_API_KEY`.
* **Upgrade de Infraestrutura (SDK `google-genai`):** Migração completa da biblioteca legada `google-generativeai` para o novo ecossistema unificado `google-genai`.
* **Compatibilidade de Modelos:** Ajuste de rotas de modelos para garantir comunicação direta com as chamadas de última geração da API do Gemini, mitigando falhas de rotas legadas (`404 v1beta not found`).

---

## 📈 Conclusões do Ciclo de Validação

**O que funcionou com excelência:**
* A leitura dinâmica dos estados das metas do JSON refletida diretamente nos componentes visuais do Streamlit.
* A blindagem das chaves de API utilizando o escopo seguro fora da pasta raiz de execução do código (`src/`).
* A velocidade de resposta do modelo após a atualização do pipeline para o SDK moderno.

**Próximos Passos para Evolução:**
* Implementar testes automatizados de asserção (via `pytest`) para validar se as respostas do modelo contêm as palavras-chave obrigatórias do JSON.
* Explorar o monitoramento de consumo de tokens utilizando ferramentas de observabilidade para LLMs à medida que o histórico do CSV escalar.