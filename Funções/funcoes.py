import json
import os

caminho = "login_finmind.json" #arquivo

def carregar_user(): #se o usuario não existir retorna lista vazia
    if not os.path.exist(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        return dados.get("usuarios", [])
    
def salvar_user(usuario, senha):
    usuarios = carregar_user() #se o usuario já existe
    for usuario in usuarios:
        if usuario["usuarios"] == usuario:
            return False #usuario já existe
        
    usuarios.append({"usuario": usuario,
                     "senha": senha})
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump({"usuarios": usuarios}, arquivo, indent=4, ensure_ascii=False)
    return True
