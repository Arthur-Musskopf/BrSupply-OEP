import streamlit as st
from langchain_openai import ChatOpenAI
from src.load_data import obter_dataframes
from src.auth import validar_usuario
from src.intent_classifier import classificar_intencao
from src.rag_chain import rag_chain
from src.pandas_agent import construir_pandas_agent
from src.session_manager import iniciar_sessao, encerrar_sessao
from src.tool_router import rotear_para_tool  # ✅ Novo import
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="BrSupplAI - SAC IFMT", layout="wide")

st.title("🤖 BrSupplAI - Agente do Supply Manager")
st.markdown("Sistema inteligente de atendimento ao IFMT - powered by BR Supply")

# Sessão de login
if "sessao" not in st.session_state:
    login = st.text_input("🔐 Digite seu login para iniciar (CPF sem pontuação):")
    if st.button("Validar acesso"):
        dfs = obter_dataframes()
        login = str(login).strip()
        if validar_usuario(login, dfs["usuarios"]):
            st.session_state.sessao = iniciar_sessao(login)
            st.session_state.dfs = dfs
            st.session_state.llm = ChatOpenAI(model="gpt-4o")
            st.session_state.pandas_agent = construir_pandas_agent(
                st.session_state.llm, dfs, login_usuario=login
            )
            st.success("Acesso autorizado. Bem-vindo!")
        else:
            st.error("Acesso negado. Contate renan.oliveira@brsupply.com.br")
    st.stop()

# Tabs principais
abas = st.tabs(["💬 Chat", "📚 Biblioteca", "📊 Histórico"])

# ABA 1: CHAT
with abas[0]:
    st.subheader("Assistente BR Supply")
    input_usuario = st.chat_input("Digite sua pergunta:")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).markdown(msg["content"])

    if input_usuario:
        st.chat_message("user").markdown(input_usuario)
        st.session_state.chat.append({"role": "user", "content": input_usuario})

        tipo = classificar_intencao(input_usuario)
        st.session_state.sessao["tipo_pergunta"] = tipo


        if "falar com" in input_usuario.lower():
            st.warning("Renan Oliveira foi notificado...")
            st.session_state.sessao["escalonamento_humano"] = True
            resposta = "Encerrando atendimento com encaminhamento para humano."

            # 🔴 Salvar log automaticamente ao escalar
            encerrar_sessao(
                st.session_state.sessao, 
                st.session_state.llm, 
                tipo_pergunta="escalonamento", 
                sucesso=False
            )

            # ⚠️ Encerrar sessão no app
            del st.session_state.sessao
            del st.session_state.chat
            st.stop()

        elif tipo == "informativa":
            resposta = rag_chain.run(input_usuario)
        else:
            resposta = rotear_para_tool(input_usuario, st.session_state.pandas_agent.tools)
            if resposta is None:
                resposta = st.session_state.pandas_agent.run(input_usuario)

        st.chat_message("assistant").markdown(resposta)
        st.session_state.chat.append({"role": "assistant", "content": resposta})
        st.session_state.sessao["historico"] = st.session_state.chat

# ABA 2: Biblioteca
with abas[1]:
    st.subheader("📚 Documentos Vetorizados")
    st.markdown("Os seguintes manuais foram vetorizados e estão disponíveis para consulta informativa via RAG:")
    st.markdown("""
    - Manual do Usuário
    - Manual - Supply Manager
    - Criação de Conta e Subconta
    - Meu Mix - Catálogo Completo
    - Dados Cadastrais BRS
    """)

# ABA 3: Histórico
with abas[2]:
    st.subheader("📊 Histórico de Sessões")
    try:
        df_logs = pd.read_csv("data/processed/logs/logs.csv")
        st.dataframe(df_logs.sort_values("fim", ascending=False), use_container_width=True)
    except Exception as e:
        st.warning(f"Não foi possível carregar o histórico. Erro: {e}")

# Encerramento manual (para simular fim de conversa)
if st.button("Encerrar Sessão"):
    encerrar_sessao(st.session_state.sessao, st.session_state.llm, st.session_state.sessao["tipo_pergunta"])
    st.success("Sessão encerrada e log salva com sucesso.")
    del st.session_state.sessao
    del st.session_state.chat