import streamlit as st
import requests as rq
import pandas as pd
import openai
import Funções.funcoes as fun
import Funções.funcoes_de_estilizacao as fe
import json

#api de inteligência artificial
openai.api_key = "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"

st.set_page_config(page_title="FinMind")
fe.titulo("FinMind", size=60, color="white")
fe.subtitulo("Sua IA de Gerenciamento Financeiro", size=20)

modo = st.radio("Escolha uma opção:", ["Login", "Cadastro"])

usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if modo == "Login":
    if st.button("Entrar"):
        if fun.validar_login(usuario, senha):
            st.success(f"Bem-vindo(a), {usuario}!")
            st.session_state["usuario_logado"] = usuario
        else:
            st.error("Usuário ou senha inválidos.")

elif modo == "Cadastro":
    if st.button("Cadastrar"):
        if len(identificador) < 3:
            st.warning("O identificador deve ter pelo menos 3 caracteres.")
        elif len(senha) < 4:
            st.warning("A senha deve ter pelo menos 4 caracteres.")
        elif "@" in identificador and not eh_email_gmail(identificador):
            st.warning("Apenas e-mails @gmail.com são permitidos.")
        elif fun.salvar_user(identificador, senha):
            st.success(" Cadastro realizado com sucesso! Você já pode fazer login.")
        else:
            st.warning("Este identificador já está em uso.")






    





