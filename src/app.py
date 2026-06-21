import streamlit as st
import pandas as pd
import json
from google import genai 
import os
from dotenv import load_dotenv

# 1. Carregar variáveis de ambiente (Chave da API do Gemini)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Erro: A variável GEMINI_API_KEY não foi encontrada no arquivo .env")
    st.stop()

client = genai.Client(api_key=api_key.strip().replace('"', '').replace("'", ""))

# 2. Configuração da Página do Streamlit
st.set_page_config(
    page_title="Agent Skopos - GenAI",
    page_icon="🤖",
    layout="wide"
)

# 3. Carregar a Base de Conhecimento (JSON e CSV)
@st.cache_data
def carregar_dados():
    try:
        with open("data/metas_usuario.json", "r", encoding="utf-8") as f:
            metas = json.load(f)
        historico = pd.read_csv("data/historico_financeiro.csv")
        return metas, historico
    except Exception as e:
        st.error(f"Erro ao carregar os arquivos de dados: {e}")
        return None, None

dados_metas, df_historico = carregar_dados()

# 4. Interface Visual - Dashboard Lateral com as Metas do Usuário
if dados_metas is not None and df_historico is not None:
    st.sidebar.header(f"👤 Usuário: {dados_metas['usuario']}")
    st.sidebar.markdown(f"**Renda Mensal:** R$ {dados_metas['renda_mensal']:.2f}")
    st.sidebar.markdown(f"**Capacidade de Poupança:** R$ {dados_metas['capacidade_poupanca_mes']:.2f}/mês")
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Suas Metas Ativas")

    # Desenha as barras de progresso para cada meta dinamicamente
    for meta in dados_metas["metas_ativas"]:
        progresso = meta["valor_atual"] / meta["valor_alvo"]
        progresso_porcentagem = min(int(progresso * 100), 100)
        
        st.sidebar.markdown(f"**{meta['descricao']}** (Prioridade: {meta['prioridade']})")
        st.sidebar.progress(progresso)
        st.sidebar.caption(
            f"Progresso: {progresso_porcentagem}% | R$ {meta['valor_atual']:.2f} de R$ {meta['valor_alvo']:.2f} | Prazo: {meta['prazo_meses']} meses"
        )
        st.sidebar.markdown("")

# 5. Configuração do Modelo Gemini com o System Prompt do Skopos
system_prompt = """
Você é o Agent Skopos, um assistente de Inteligência Artificial Generativa altamente estratégico, especializado em análise de dados financeiros e planejamento preditivo de metas. Seu propósito é guiar o usuário para que ele atinja seus objetivos de vida de forma realista.

Você receberá dados do perfil do usuário, capacidade de poupança, metas ativas e o histórico recente de transações.

Diretrizes:
- Atue como um mentor focado no futuro. Seja proativo e analítico.
- Sempre utilize marcadores (bullet points), negritos e dados percentuais para respostas escaneáveis.
- REGRA DE OURO:
 Nunca entregue um diagnóstico negativo sem apresentar uma alternativa de solução (ex: sugerir cortes em categorias supérfluas do CSV como Lazer ou Delivery). 
 Jamais responda fora do tema proposto.
- Só recomende alocações com base nos prazos do JSON (Curto prazo = liquidez diária, longo prazo = indexados à inflação), quando for perguntado.
"""


# Consolidar a base de conhecimento textual para injetar no Gemini
contexto_dados = f"""
[BASE DE CONHECIMENTO DO USUÁRIO]
Dados de Metas (JSON):
{json.dumps(dados_metas, indent=2, ensure_ascii=False)}

Histórico de Transações (CSV):
{df_historico.to_string(index=False)}
"""

# 6. Área do Chat Principal
st.title("🎯 Agent Skopos — Planejador Estratégico de Metas")
st.markdown("Bem-vindo ao seu painel preditivo. Pergunte ao agente sobre a saúde das suas metas, projeções de prazos ou onde ajustar o seu orçamento atual.")

# Inicializar o histórico de chat do Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens anteriores do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar a interação do usuário
if prompt := st.chat_input("Ex: Vou conseguir bater a meta do meu Notebook no prazo atual?"):
    # Exibir pergunta do usuário no chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gerar a resposta do Gemini injetando o contexto de dados
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔄 Analisando seus dados e calculando projeções...")
        
        try:
            # Junta o contexto estrito dos arquivos com a pergunta que o usuário digitou no chat
            prompt_completo = f"Contexto atual dos dados do usuário:\n{contexto_dados}\n\nPergunta do usuário: {prompt}"
            
            # Nova chamada oficial da biblioteca google-genai
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt_completo,
                config={
                        'system_instruction': system_prompt,
                    }
            )
            resposta_ia = response.text
            
            message_placeholder.markdown(resposta_ia)
            st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
            
        except Exception as e:
            message_placeholder.markdown(f"❌ Desculpe, ocorreu um erro ao processar sua resposta: {e}")