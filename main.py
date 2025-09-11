import streamlit as st
import requests as rq
import pandas as pd
import openai
import Funções.funcoes as fun
import json

#api de inteligência artificial
openai.api_key = "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"

st.set_page_config(page_title="FinMind")
fe.titulo("FinMind", size=60, color="white")
fe.subtitulo("Sua IA de Gerenciamento Financeiro", size=20)

modo = st.radio("Escolha uma opção:", ["Login", "Cadastro"])

usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="senha")

if modo == "Login":
    if st.button("Entrar"):
        if fun.validar_login(usuario, senha):
            st.success(f"Bem-vindo(a), {usuario}!")
            st.session_state["usuario_logado"] = usuario
        else:
            st.error("Usuário ou senha inválidos.")

elif modo == "Cadastro":
    if st.button("Cadastrar"):
        if fun.salvar_user(usuario, senha):
            st.success("Cadastro realizado com sucesso! Você já pode fazer login.")
        else:
            st.warning("Este nome de usuário já está em uso.")







    


