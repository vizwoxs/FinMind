import funcoes as fun


def menu():
    print("\n=== FinMind - Teste de Login e Cadastro ===")
    print("1. Cadastrar novo usuário")
    print("2. Fazer login")
    print("3. Mostrar todos os usuários")
    print("0. Sair")

while True:
    menu()
    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        username = input("Novo usuário: ")
        password = input("Nova senha: ")
        if fun.salvar_user(username, password):
            print("✅ Usuário cadastrado com sucesso!")
        else:
            print("⚠️ Usuário já existe.")

    elif escolha == "2":
        username = input("Usuário: ")
        password = input("Senha: ")
        if fun.validar_login(username, password):
            print(f"🔓 Login bem-sucedido! Bem-vinda, {username}.")
        else:
            print("❌ Usuário ou senha inválidos.")

    elif escolha == "3":
        usuarios = fun.carregar_user()
        print("\n📋 Lista de usuários cadastrados:")
        for u in usuarios:
            print(f" - {u['username']}")
        if not usuarios:
            print("Nenhum usuário cadastrado ainda.")

    elif escolha == "0":
        print("👋 Encerrando teste. Até mais!")
        break

    else:
        print("Opção inválida. Tente novamente.")

    
