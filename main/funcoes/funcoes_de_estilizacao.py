import streamlit as st

def titulo(text, size=50, color="white", align="center"):
    st.markdown(f"""
    <h1 style='text-align: {align}; 
                color: {color}; 
                font-siz\e: {size}px;
                font-family: "Source Sans Pro", sans-serif'>
        {text}
    </h1>
    """, unsafe_allow_html=True)

import streamlit as st

def subtitulo(text, size=24, color="white", align="center", bottom_margin=10):
    st.markdown(f"""
    <h2 style='text-align: {align}; color: {color}; 
                font-size: {size}px; font-weight: 400;
                margin-top: 0; margin-bottom: {bottom_margin}px;
                font-family: "Source Sans Pro", sans-serif'>
        {text}
    </h2>
    """, unsafe_allow_html=True)


def construir_balao_chat(msg):
    if msg["role"] == "user":
        return f"""
        <div style='background-color:#3A3A3A; color:#FFFFFF; 
                    padding:16px 20px; border-radius:20px; 
                    margin:12px 0; max-width:75%; 
                    font-family:Arial, sans-serif; font-size:16px;
                    float:right; clear:both;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
            {msg['content']}
        </div>
        """
    elif msg["role"] == "assistant":
        return f"""
        <div style='background-color:#222222; color:#E5E5E5; 
                    padding:16px 20px; border-radius:20px; 
                    margin:12px 0; max-width:75%; 
                    font-family:Arial, sans-serif; font-size:16px;
                    float:left; clear:both;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
            {msg['content']}
        </div>
        """
    else:
        return f"<div>{msg['content']}</div>"


def exibir_logo():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 10px;'>
            <img src="https://i.postimg.cc/cJ88nkxT/Fin-Mind-Logo-3.png" alt="FinMind Logo" style="width: 250px; height: auto;">
        </div>
    """, unsafe_allow_html=True)

def footer():
    st.markdown("""
    <div style='text-align: center; margin-top: 20px; font-size: 12px; color: gray;'>
        <img src="https://i.postimg.cc/mgKPB3Y9/Design-sem-nome-1.png" alt="FinMind Logo" style="width: 200px; height: auto; margin-bottom: 5px;">
    </div>
    """, unsafe_allow_html=True)

def background_login(imagem_url="https://i.postimg.cc/bJ1PkkSK/Black-Blue-Futuristic-Technology-Presentation.jpg", cor="#181920"):
    """
    Aplica um background na tela de login.
    Usa a imagem fornecida por padrão.
    """
    if imagem_url:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url('{imagem_url}') no-repeat center center fixed;
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: {cor};
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
