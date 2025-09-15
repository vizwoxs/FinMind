import json
import os
import streamlit as st
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDbUr0HPtRhdkz3R4n5NOL7Ncj2kU_uIf8" #modelo padrão

gemini_configurado = False #se o gemini foi configurado
model = None 

#função da funcionalidade da chave
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel() #modelo da ia
        gemini_configurado = True #Indica que o Gemini foi configurado com sucesso
    except Exception as e:
        st.error(f"Erro ao configurar Gemini: {e}") #Indica que houve um erro na configuração

else:
    st.warning("Nenhuma chave Gemini encontrada. Configure a variável de ambiente GEMINI_API_KEY.") #Aviso se a chave não estiver configurada

#função de login do user
def carregar_user():# Carrega a lista de usuários do arquivo JSON
    if not os.path.exists(CAMINHO): #se o usuário não existir
        return [] #retorna lista vazia
    try: #caso de certo
        with open(CAMINHO, "r", encoding="utf-8") as arquivo: #abre o arquivo
            return json.load(arquivo).get("usuarios", []) #retorna a lista de usuários
    except (json.JSONDecodeError, FileNotFoundError): #caso de erro
        return [] #retorna lista vazia

def salvar_user(user, senha): # Salva um novo usuário no arquivo JSON
    usuarios = carregar_user()
    if any(u["usuario"] == user for u in usuarios): #ternario
        return False
    usuarios.append({"usuario": user, "senha": senha})
    with open(CAMINHO, "w", encoding="utf-8") as arquivo:
        json.dump({"usuarios": usuarios}, arquivo, indent=4, ensure_ascii=False) #adiciona dentro do arquivo
    return True

def validar_login(user, senha): # Valida o login do usuário
    return any(u["usuario"] == user and u["senha"] == senha for u in carregar_user()) #terrnario
