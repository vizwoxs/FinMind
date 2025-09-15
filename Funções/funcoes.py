# app.py

import os
import json
import bcrypt
import mimetypes
from pathlib import Path

import streamlit as st
from google import genai
from google.genai import types

# ─── Configurações gerais ──────────────────────────────────────────────────────

# Carrega a chave a partir de variáveis de ambiente ou de st.secrets
API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]

# Caminho absoluto para o JSON de usuários
DATA_PATH = Path(__file__).parent / "../API-login/login_finmind.json"

SYSTEM_PROMPT = """
Você é o FinMind, um assistente financeiro inteligente, didático e empático.
Seu papel é ajudar usuários brasileiros a entender, organizar e melhorar suas finanças pessoais.
Sempre responda em português do Brasil, de forma clara e adaptada ao nível de conhecimento do usuário.

🎭 Tom de comunicação
- Se o usuário demonstrar ansiedade, medo ou estresse → responda com empatia antes de dicas.
- Se pedir conselhos técnicos → seja claro e objetivo, usando dados organizados.
- Se pedir motivação → use um tom amigável e encorajador.

📊 Áreas de apoio
1. Orçamento e controle de gastos
2. Dívidas e crédito
3. Investimentos
4. Economia do dia a dia
5. Planejamento de metas
6. Impostos e burocracias
7. Saúde emocional com dinheiro

📌 Regras
- Sempre dê exemplos práticos.
- Para cálculos, mostre passo a passo.
- Se a pergunta for vaga, solicite mais detalhes.
- Finalize com sugestão de próximo passo.
- Não repita informações já dadas.
"""

# ─── Utils de arquivo e hashing ─────────────────────────────────────────────────

def save_binary_file(file_name: str, data: bytes):
    """Salva bytes em arquivo binário e exibe caminho."""
    Path(file_name).write_bytes(data)
    st.write(f"Imagem salva em: `{file_name}`")

def carregar_user() -> list[dict]:
    """Carrega lista de usuários cadastrados (com hash de senha)."""
    if not DATA_PATH.exists():
        return []
    try:
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        return data.get("usuarios", [])
    except (json.JSONDecodeError, OSError):
        return []

def salvar_user(usuario: str, senha: str) -> bool:
    """Registra novo usuário com senha hasheada. Retorna False se existir."""
    usuarios = carregar_user()
    if any(u["usuario"] == usuario for u in usuarios):
        return False
    hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    usuarios.append({"usuario": usuario, "senha_hash": hashed})
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps({"usuarios": usuarios}, indent=4, ensure_ascii=False), encoding="utf-8")
    return True

def validar_login(usuario: str, senha: str) -> bool:
    """Valida credenciais comparando hash."""
    for u in carregar_user():
        if u["usuario"] == usuario and bcrypt.checkpw(senha.encode("utf-8"), u["senha_hash"].encode("utf-8")):
            return True
    return False

def eh_email_gmail(email: str) -> bool:
    """Verifica se é um e-mail @gmail.com."""
    return email.lower().endswith("@gmail.com")

# ─── Inicialização do client Gemini ────────────────────────────────────────────

@st.cache_resource
def init_genai_client() -> genai.Client | None:
    try:
        return genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"Falha ao inicializar Gemini: {e}")
        return None

client = init_genai_client()

# ─── Função principal de chat com Gemini ────────────────────────────────────────

def responder_gemini(mensagem: str) -> str | None:
    """
    Envia mensagem ao modelo Gemini que pode retornar texto e imagens.
    Salva imagens localmente e exibe no Streamlit.
    """
    if client is None:
        st.warning("Gemini não está configurado.")
        return None

    # Inicializa histórico de conteúdo
    if "gemini_history" not in st.session_state:
        st.session_state.gemini_history = [
            types.Content(role="system", parts=[types.Part.from_text(SYSTEM_PROMPT)])
        ]

    # Acrescenta mensagem do usuário
    st.session_state.gemini_history.append(
        types.Content(role="user", parts=[types.Part.from_text(mensagem)])
    )

    generate_config = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        max_output_tokens=600,
        temperature=0.7,
    )

    resposta_texto = ""
    imagens_salvas: list[str] = []

    # Streaming de resposta
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash-image-preview",
        contents=st.session_state.gemini_history,
        config=generate_config,
    ):
        candidate = chunk.candidates[0].content
        for part in candidate.parts:
            # Parte com imagem
            if part.inline_data and part.inline_data.data:
                ext = mimetypes.guess_extension(part.inline_data.mime_type) or ".bin"
                nome = f"gemini_img_{len(imagens_salvas)}{ext}"
                save_binary_file(nome, part.inline_data.data)
                imagens_salvas.append(nome)
            # Parte com texto
            elif part.text:
                resposta_texto += part.text

    # Exibe imagens no Streamlit
    for img in imagens_salvas:
        st.image(img)

    return resposta_texto.strip() or None

# ─── Fallback estático de intenções ────────────────────────────────────────────

def proxima_pergunta(estado: dict) -> str:
    if not estado.get("falou_renda"):
        return "Me conte sobre sua renda mensal."
    elif not estado.get("falou_dívida"):
        return "Você possui dívidas atualmente? Se sim, quais?"
    elif not estado.get("falou_metas"):
        return "Quais são suas principais metas financeiras?"
    else:
        return "Se quiser, posso te ajudar a analisar seus gastos ou sugerir investimentos!"

def responder_fallback(mensagem: str, historico: list) -> tuple[str, list]:
    mensagens = {
        "oi": "Oi! Como posso te ajudar com suas finanças hoje?",
        "ajuda": "Diga se prefere falar de orçamento, dívidas ou investimentos.",
        "default": "Conte mais sobre sua situação financeira: renda, dívidas, metas..."
    }
    msg = mensagem.lower()
    chave = next((k for k in mensagens if f" {k} " in f" {msg} "), None)
    if chave is None:
        resposta = proxima_pergunta(historico[-1].get("estado", {}))
    else:
        resposta = mensagens[chave]
    estado = historico[-1].get("estado", {}) if historico else {}
    if chave:
        estado[f"falou_{chave}"] = True
    historico.append({"role": "user", "content": mensagem})
    historico.append({"role": "assistant", "content": resposta, "estado": estado})
    return resposta, historico

# ─── Função de interface principal ─────────────────────────────────────────────

def responder_chat(mensagem: str):
    historico = st.session_state.get("messages", [])
    resp = responder_gemini(mensagem)
    if resp is not None:
        historico.append({"role": "user", "content": mensagem})
        historico.append({"role": "assistant", "content": resp})
        st.session_state.messages = historico
        return resp
    # fallback
    fallback_resp, hist = responder_fallback(mensagem, historico)
    st.session_state.messages = hist
    return fallback_resp

# ─── Streamlit UI ──────────────────────────────────────────────────────────────

st.title("FinMind: Assistente Financeiro")

menu = st.sidebar.selectbox("Menu", ["Login", "Cadastrar", "Chat"])
if menu == "Login":
    u = st.text_input("Usuário (e-mail Gmail)", "")
    p = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if validar_login(u, p) and eh_email_gmail(u):
            st.success("Login bem-sucedido!")
            st.session_state.authenticated = True
        else:
            st.error("Falha ao autenticar. Verifique credenciais ou domínio do e-mail.")
elif menu == "Cadastrar":
    u = st.text_input("Novo usuário (e-mail Gmail)", "")
    p = st.text_input("Nova senha", type="password")
    if st.button("Registrar"):
        if not eh_email_gmail(u):
            st.error("Use um e-mail @gmail.com.")
        elif salvar_user(u, p):
            st.success("Usuário cadastrado com sucesso!")
        else:
            st.warning("Usuário já existe.")
else:
    if st.session_state.get("authenticated"):
        pergunta = st.text_input("Você:", "")
        if st.button("Enviar"):
            resposta = responder_chat(pergunta)
            st.markdown(f"**FinMind:** {resposta}")
    else:
        st.warning("Faça login para começar a conversar.")
```
