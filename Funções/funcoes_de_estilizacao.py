import streamlit as st

def titulo(text, size=50, color="white", align="center"):
    st.markdown(f"""
    <h1 style='text-align: {align}; 
                color: {color}; 
                font-size: {size}px;
                font-family: "Source Sans Pro", sans-serif'>
        {text}
    </h1>
    """, unsafe_allow_html=True)

import streamlit as st

def subtitulo(text, size=24, color="white", align="center", bottom_margin=20):
    st.markdown(f"""
    <h2 style='text-align: {align}; color: {color}; 
                font-size: {size}px; font-weight: 400;
                margin-top: 0; margin-bottom: {bottom_margin}px;
                font-family: "Source Sans Pro", sans-serif'>
        {text}
    </h2>
    """, unsafe_allow_html=True)


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


