import json
import os
import streamlit as st
import google.generativeai as genai
import re

# Use o modelo padrão disponível (exemplo: gemini-1.0-pro)
GEMINI_API_KEY = "AIzaSyBWPQm57MooUVfRuqpEglEFewIX6HXvTMU"

gemini_configurado = False #
model = None

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel() #modelo da ia
        gemini_configurado = True # Indica que o Gemini foi configurado com sucesso
    except Exception as e:
        st.error(f"Erro ao configurar Gemini: {e}") # Indica que houve um erro na configuração

else:
    st.warning("Nenhuma chave Gemini encontrada. Configure a variável de ambiente GEMINI_API_KEY.") # Aviso se a chave não estiver configurada

# Caminho para o arquivo JSON que armazena os usuários
CAMINHO = os.path.join(os.path.dirname(__file__), "../API-login/login_finmind.json")

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

def responder_gemini(prompt):
    if not gemini_configurado or model is None:
        return None
    try:
        descricao_ia = (
            "Você é um assistente financeiro virtual chamado FinMind, "
            "especialista em finanças pessoais, que responde sempre em português brasileiro, "
            "de forma clara, amigável e objetiva. "
            "Ajude o usuário a organizar suas finanças, tirar dúvidas e alcançar metas." 
            "Forneça dicas práticas e estratégias financeiras personalizadas."
            "Você não é capaz de responder perguntas que não sejam do ramo financeiro"
            "Não é necessário fazer uma saudação inicial em todas as respostas, vá direto ao ponto."
            "Lembre-se de conversas anteriores para manter o contexto."
            "Seja empático e encorajador, ajudando o usuário a se sentir no controle de suas finanças." 
            "Faça calculos quando necessário."
        )
        prompt_final = f"{descricao_ia}\n\nPergunta do usuário: {prompt}"
        response = model.generate_content(prompt_final)
        return response.text
    except Exception as e:
        st.warning(f"Erro ao gerar resposta com Gemini: {e}")
        return None

def responder_chat(mensagem, historico=None):
    """
    Tenta usar o Gemini e, em caso de falha, usa o fallback local.
    Sempre retorna (resposta, historico_atualizado).
    """
    if historico is None:
        historico = st.session_state.get("chat_history", [])
    resposta_gemini = responder_gemini(mensagem)
    if resposta_gemini:
        historico.append({"role": "user", "content": remover_tags_html(mensagem)})
        historico.append({"role": "assistant", "content": remover_tags_html(resposta_gemini)})
        st.session_state.chat_history = historico
        return resposta_gemini, historico

    resposta, historico_atualizado = responder_fallback(mensagem, historico)
    st.session_state.chat_history = historico_atualizado
    return resposta, historico_atualizado

def responder_fallback(mensagem, historico):
    mensagem_lower = mensagem.lower()
    respostas = {
        "saudacao": "Oi! Que bom te ver por aqui. Como posso te ajudar com suas finanças hoje?",
        "ajuda": "Claro! Me diz com o que você precisa de ajuda: orçamento, dívidas, metas ou outra coisa?",
        "orçamento": "Regra 50-30-20: 50% necessidades, 30% desejos, 20% investimentos.",
        "dívida": "Liste suas dívidas, priorize as de maior juros e evite novas.",
        "investir": "Comece pela reserva de emergência. Depois pense em Tesouro ou ETFs.",
        "economizar": "Use lista de compras, corte delivery, cancele assinaturas desnecessárias.",
        "cartão": "Use até 30% do limite e pague sempre a fatura inteira.",
        "metas": "Me conte uma meta e vamos traçar um plano juntos.",
        "imposto": "Se for IR, lembre-se de declarar rendimentos, investimentos e despesas dedutíveis.",
        "emoções": "É normal sentir ansiedade com dinheiro. Vamos organizar passo a passo.",
        "dicas": "Prefere dicas para economizar, investir ou quitar dívidas?",
        "simular": "Me diga quanto quer juntar e em quantos meses para eu calcular.",
        "analisar": "Posso analisar seus gastos e sugerir cortes. Quer ver um gráfico?",
        "default": "Me conte mais sobre sua situação financeira: renda, dívidas, metas..."
    }

def botao_reiniciar_chat():
    if "historico_conversas" not in st.session_state:
        st.session_state.historico_conversas = []
    if st.button("Novo Chat"):
        # Salva o chat atual no histórico, se houver mensagens
        if st.session_state.chat_history:
            st.session_state.historico_conversas.append(list(st.session_state.chat_history))
        st.session_state.chat_history = []
        st.rerun()

def mostrar_historico_conversas():
    for i, conversa in enumerate(st.session_state.historico_conversas):
        st.markdown(f"**Chat {i+1}:**")
        for msg in conversa:
            st.markdown(f"- {msg['role']}: {msg['content']}")

def remover_tags_html(texto):
    return re.sub(r'<.*?>', '', texto)


