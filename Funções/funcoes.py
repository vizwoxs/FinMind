import json
import os
import streamlit as st
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDbUr0HPtRhdkz3R4n5NOL7Ncj2kU_uIf8" #modelo padrão

gemini_configurado = False #se o gemini foi configurado
model = None 

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel() #modelo da ia
        gemini_configurado = True #Indica que o Gemini foi configurado com sucesso
    except Exception as e:
        st.error(f"Erro ao configurar Gemini: {e}") #Indica que houve um erro na configuração

else:
    st.warning("Nenhuma chave Gemini encontrada. Configure a variável de ambiente GEMINI_API_KEY.") #Aviso se a chave não estiver configurada
