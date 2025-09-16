# FinMind

FinMind é um assistente virtual de finanças pessoais, desenvolvido em Python com Streamlit e integração à IA generativa Gemini (Google Generative AI). O projeto oferece um chat inteligente para tirar dúvidas financeiras, organizar gastos, simular metas e muito mais, com interface moderna, login seguro e histórico de conversas.

---

## ✨ Funcionalidades

- **Chat inteligente** com IA Gemini (Google Generative AI)
- **Login de usuário** com cadastro e validação
- **Histórico de conversas** salvo por sessão
- **Interface moderna** com balões de chat estilizados e background customizável
- **Exemplo de histórico financeiro** para testes e simulações
- **Botão de novo chat** que salva o histórico anterior
- **Mensagens de espera** enquanto a IA responde
- **Suporte a português brasileiro**

---

## 🚀 Como rodar o projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seuusuario/finmind.git
   cd finmind
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure sua chave da API Gemini:**
   - Obtenha uma chave no [Google Cloud Console](https://aistudio.google.com/app/apikey).
   - Coloque a chave no arquivo `funcoes/funcoes.py` na variável `GEMINI_API_KEY`.

4. **Execute o app:**
   ```bash
   streamlit run main.py
   ```

---

## 🗂 Estrutura do Projeto

```
FinMind/
│ main.py
│ requirements.txt
│ login_finmind.json
│ descobertas.txt
│
├─ funcoes/
│    ├─ funcoes.py
│    └─ funcoes_de_estilizacao.py
│
├─ assets/
│    └─ finmindlogo.png
```

---

## 📝 Observações Técnicas

- O arquivo `login_finmind.json` armazena usuários e senhas em formato JSON.
- O parâmetro `indent=4` deixa o JSON legível.
- `ensure_ascii=False` permite acentos e caracteres especiais no JSON.
- `st.session_state` gerencia o estado do chat e histórico entre interações.
- `unsafe_allow_html=True` permite HTML customizado nos balões de chat.
- O histórico financeiro de exemplo é criado com pandas e cacheado para performance.

---

## 💡 Dicas de Uso

- Para trocar o background, altere a URL na função `background_login` em `funcoes_de_estilizacao.py`.
- Para personalizar a IA, edite o prompt na função `responder_gemini` em `funcoes.py`.
- O botão "Novo Chat" salva o chat atual no histórico antes de limpar.

---

## 👩‍💻 Contribuição

Sinta-se à vontade para abrir issues, sugerir melhorias ou enviar pull requests!

---

## 📄 Licença

Este projeto está sob a licença MIT.

---

**FinMind** — Seu assistente financeiro inteligente! - vizwoxs & DEVdamas9
