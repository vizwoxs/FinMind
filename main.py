
import pandas as pd
import streamlit as st
import Funções.funcoes as fun
import Funções.funcoes_de_estilizacao as fe

st.set_page_config(page_title="FinMind", layout="wide")


def mostrar_chat(chat_history):
    for msg in chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style='background-color:#2D2D2D; color:#FFFFFF; 
                        padding:10px 14px; border-radius:18px; 
                        margin:8px 0; max-width:60%; 
                        font-family:Arial, sans-serif; font-size:14px;
                        float:right; clear:both;'>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)

        elif msg["role"] == "assistant":
            st.markdown(f"""
            <div style='background-color:#1E1E1E; color:#E5E5E5; 
                        padding:10px 14px; border-radius:18px; 
                        margin:8px 0; max-width:60%; 
                        font-family:Arial, sans-serif; font-size:14px;
                        float:left; clear:both;'>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)


if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "historico_financeiro" not in st.session_state:
    @st.cache_data
    def carregar_dados_exemplo():
        return pd.DataFrame({
            "Data": ["2025-09-01", "2025-09-05", "2025-09-10"],
            "Categoria": ["Alimentação", "Transporte", "Lazer"],
            "Valor": [120.50, 45.00, 80.00]
        })
    st.session_state.historico_financeiro = carregar_dados_exemplo()


if st.session_state.usuario_logado is None:
    fe.titulo("FinMind", size=60, color="white")
    fe.subtitulo("Sua IA de Gerenciamento Financeiro", size=20)

    modo = st.radio("Escolha uma opção:", ["Login", "Cadastro"])
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if modo == "Login":
        if st.button("Entrar"):
            if fun.validar_login(usuario, senha):
                st.session_state.usuario_logado = usuario
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

    elif modo == "Cadastro":
        if st.button("Cadastrar"):
            if len(usuario) < 3:
                st.warning("O identificador deve ter pelo menos 3 caracteres.")
            elif len(senha) < 4:
                st.warning("A senha deve ter pelo menos 4 caracteres.")
            elif "@" in usuario and not fun.eh_email_gmail(usuario):
                st.warning("Apenas e-mails @gmail.com são permitidos.")
            elif fun.salvar_user(usuario, senha):
                st.success("Cadastro realizado com sucesso! Faça login.")
            else:
                st.warning("Este identificador já está em uso.")
else:


    fe.titulo(f"Olá, {st.session_state.usuario_logado}!")
    fe.subtitulo("Digite sua dúvida financeira abaixo:")

    user_input = st.chat_input("Pergunte algo sobre seu dinheiro...")

    if user_input:
        resposta, st.session_state.chat_history = fun.responder_chat(
            user_input, st.session_state.chat_history
        )

 
    mostrar_chat(st.session_state.chat_history)
