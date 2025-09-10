import json
import os

caminho = "login_finmind.json" #arquivo

def carregar_user(): #se o usuario não existir retorna lista vazia
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo) #converter o arquivo em um dicionário em python
        return dados.get("usuarios", []) #retorna a lista de usuario dentro da chave, se não existir retorna lista vazia
    
def salvar_user(user, senha):
    usuarios = carregar_user() #se o usuario já existe, se não retorna false como falha de cadastro
    for usuario in usuarios:
        if usuario["usuario"] == user:
            return False #usuario já existe
        
    usuarios.append({"usuario": user,
                     "senha": senha})
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump({"usuarios": usuarios}, arquivo, indent=4, ensure_ascii=False)
    return True

def validar_login(user, senha): #carrega usuarios cadastrados
    usuarios = carregar_user() #percorre a lista verificando
    for usuario in usuarios:
        if usuario["usuario"] == user and usuario["senha"] == senha:
            return True #login valido
    return "Esse usuario não existe" #login invalido
