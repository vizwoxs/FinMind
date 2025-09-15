import json
import os
import streamlit as st
import google.generativeai as genai


GEMINI_API_KEY = ""

gemini_configurado = False
model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-pro")
        gemini_configurado = True
    except Exception as e:
        st.error(f"Erro ao configurar Gemini: {e}")
else:
    st.warning("Nenhuma chave Gemini encontrada. Configure a variável de ambiente GEMINI_API_KEY.")


CAMINHO = "login_finmind.json"


def carregar_user():
    if not os.path.exists(CAMINHO):
        return []
    try:
        with open(CAMINHO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo).get("usuarios", [])
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def salvar_user(user, senha):
    usuarios = carregar_user()
    if any(u["usuario"] == user for u in usuarios):
        return False
    usuarios.append({"usuario": user, "senha": senha})
    with open(CAMINHO, "w", encoding="utf-8") as arquivo:
        json.dump({"usuarios": usuarios}, arquivo, indent=4, ensure_ascii=False)
    return True

def validar_login(user, senha):
    return any(u["usuario"] == user and u["senha"] == senha for u in carregar_user())

def eh_email_gmail(email):
    return email.lower().endswith("@gmail.com")


def responder_gemini(mensagem):
    """
    Usa o objeto de chat do Gemini para gerenciar o histórico da conversa.
    O histórico é armazenado na sessão do Streamlit.
    """
    if not gemini_configurado:
        st.warning("Gemini não está configurado.")
        return None


    system_prompt = """
Você é o **FinMind**, um assistente financeiro inteligente, didático e empático.
Seu papel é ajudar usuários brasileiros a entender, organizar e melhorar suas finanças pessoais.
Sempre responda em português do Brasil, de forma clara e adaptada ao nível de conhecimento do usuário.

🎭 **Tom de comunicação**
- Se o usuário demonstrar ansiedade, medo, estresse ou preocupação → responda com empatia, acolhendo as emoções antes de dar conselhos técnicos.
- Se o usuário pedir conselhos técnicos (ex.: investimentos, dívidas, orçamento) → responda com clareza, objetividade e dados organizados.
- Se o usuário pedir motivação ou ajuda com hábitos → use um tom amigável e encorajador.

📊 **Áreas de apoio:**
1. Orçamento e controle de gastos
2. Dívidas e crédito
3. Investimentos
4. Economia do dia a dia
5. Planejamento de metas
6. Impostos e burocracias
7. Saúde emocional com dinheiro

📌 **Regras importantes:**
- Sempre dê exemplos práticos, mesmo que hipotéticos.
- Se o usuário pedir cálculos (ex.: quanto guardar por mês), faça a conta passo a passo.
- Se a pergunta for vaga, peça mais informações antes de responder.
- Sempre finalize sua resposta com uma **sugestão de próximo passo**.
- **Regra anti-repetição:** Evite repetir informações que já foram discutidas. Mantenha o fluxo da conversa.
"""
    

    if "gemini_chat" not in st.session_state:
        st.session_state.gemini_chat = model.start_chat(history=[

            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["Ok, entendi. Estou pronto para começar."]}
        ])

    try:
 
        response = st.session_state.gemini_chat.send_message(
            mensagem,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=600,
                temperature=0.7
            )
        )
        return response.text.strip()
    
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return None


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

    chave = next((k for k, _ in respostas.items() if k in mensagem_lower), None)
    estado = historico[-1].get("estado", {}) if historico else {}

    if chave:
        estado[f"falou_{chave}"] = True

    if not chave:
        resposta = proxima_pergunta(estado)
    else:
        resposta = respostas[chave]

    if historico and historico[-1].get("content") == resposta:
        resposta = "Tem mais algum detalhe que você gostaria de compartilhar sobre sua situação financeira?"

    return resposta, historico + [
        {"role": "user", "content": mensagem},
        {"role": "assistant", "content": resposta, "estado": estado},
    ]

def atualizar_estado(historico, chave, valor=True):
    estado = historico[-1].get("estado", {}) if historico else {}
    estado[chave] = valor
    return estado

def proxima_pergunta(estado):
    if not estado.get("falou_renda"):
        return "Me conte sobre sua renda mensal."
    elif not estado.get("falou_dívida"):
        return "Você possui dívidas atualmente? Se sim, quais?"
    elif not estado.get("falou_metas"):
        return "Quais são suas principais metas financeiras?"
    else:
        return "Se quiser, posso te ajudar a analisar seus gastos ou sugerir investimentos!"


def responder_chat(mensagem, historico=None):
    if historico is None:
        historico = st.session_state.get("messages", [])
    resposta_gemini = responder_gemini(mensagem)
    if resposta_gemini:
        historico.append({"role": "user", "content": mensagem})
        historico.append({"role": "assistant", "content": resposta_gemini})
        st.session_state.messages = historico
        return resposta_gemini, historico

    resposta, historico_atualizado = responder_fallback(mensagem, historico)
    st.session_state.messages = historico_atualizado
    return resposta, historico_atualizado


