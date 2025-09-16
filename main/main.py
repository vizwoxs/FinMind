import pandas as pd
import streamlit as st
from funcoes import funcoes as fun
from funcoes import funcoes_de_estilizacao as fe
import time

#titulo e largura
st.set_page_config(page_title="FinMind", layout="wide")

#percorre as mensagens e exibe com balões estilizados
def mostrar_chat(chat_historico):
    for msg in chat_historico:
        st.markdown(fe.construir_balao_chat(msg), unsafe_allow_html=True)

#funções funcionando
if "historico_conversas" not in st.session_state:
    st.session_state.historico_conversas = []
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None
if "chat_historico" not in st.session_state:
    st.session_state.chat_historico = []
if "historico_financeiro" not in st.session_state:
    @st.cache_data #amarzenar em cache para não recarregar toda hora

    def carregar_dados_exemplo(): #simula o carregamento de dados financeiros
        return pd.DataFrame({
            "Data": ["2025-09-01", "2025-09-05", "2025-09-10"],
            "Categoria": ["Alimentação", "Transporte", "Lazer"],
            "Valor": [120.50, 45.00, 80.00]
        })
    st.session_state.historico_financeiro = carregar_dados_exemplo()

#inicio de da pagina de login
if st.session_state.usuario_logado is None:
    fe.background_login(imagem_url="https://i.postimg.cc/Kc62Q9DC/Design-sem-nome-3.png")
    fe.exibir_logo()
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
            if not usuario or not senha:
                st.warning("Preencha usuário e senha.")
            elif len(usuario) < 3:
                st.warning("O identificador deve ter pelo menos 3 caracteres.")
            elif len(senha) < 4:
                    st.warning("A senha deve ter pelo menos 4 caracteres.")
            else:
                try:
                    if fun.salvar_user(usuario, senha):
                        st.success("Cadastro realizado com sucesso! Faça login.")
                    else:
                        st.warning("Este identificador já está em uso.")
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {e}")


else: #barra lateral e chat

    with st.sidebar.expander("Histórico de Conversa", expanded=True):
        if st.session_state.historico_conversas or st.session_state.chat_historico:

            for idx, conversa in enumerate(st.session_state.historico_conversas): #mostra todas as conversas anteriores
                st.markdown(f"---\n**Conversa {idx+1}:**")
                for msg in conversa:
                    st.markdown(f"**{'Você' if msg['role']=='user' else 'FinMind'}:** {msg['content']}")
        #mostra o chat atual se houver
        if st.session_state.chat_historico:
            st.markdown("---\n**Conversa atual:**")
            for msg in st.session_state.chat_historico:
                st.markdown(f"**{'Você' if msg['role']=='user' else 'FinMind'}:** {msg['content']}")
        else:
            st.info("Nenhuma conversa registrada ainda.")
            

    fun.botao_reiniciar_chat()
    
    fe.footer()
    fe.titulo(f"Olá, {st.session_state.usuario_logado}!")
    fe.subtitulo("Digite sua dúvida financeira abaixo:")

    user_input = st.chat_input("Pergunte algo sobre seu dinheiro...")

    if user_input:
        with st.spinner("..."):
            time.sleep(2)
            resposta, st.session_state.chat_historico = fun.responder_chat(
                user_input, st.session_state.chat_historico
        )

    mostrar_chat(st.session_state.chat_historico)
