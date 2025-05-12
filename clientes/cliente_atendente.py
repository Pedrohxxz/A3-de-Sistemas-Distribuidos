import socket

HOST = "localhost"
PORT = 12345


def exibir_menu_atendente():
    print("--- Cliente Atendente ---")
    print("1. Criar Reserva")
    print("2. Cancelar Reserva")
    print("3. Sair")
    return input("Escolha uma opção: ")


def atendente_criar_reserva():
    data = input("Data (dd/mm/aaaa): ")
    hora = input("Hora (hh:mm): ")
    numero_mesa = int(input("Número da mesa: "))
    quantidade = int(input("Quantidade de pessoas: "))
    nome = input("Nome do responsável: ")
    return f"ATENDENTE_CRIAR;{data};{hora};{numero_mesa};{quantidade};{nome}"


def atendente_cancelar_reserva():
    data = input("Data (dd/mm/aaaa): ")
    hora = input("Hora (hh:mm): ")
    numero_mesa = input("Número da mesa: ")
    nome = input("Nome do responsável: ")
    return f"ATENDENTE_CANCELAR;{data};{hora};{numero_mesa};{nome}"


def enviar_mensagem(mensagem):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((HOST, PORT))
            cliente.sendall(mensagem.encode())
            resposta = cliente.recv(1024).decode()
            print(f"[RESPOSTA] {resposta}")
    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor.")


def main():
    while True:
        opcao = exibir_menu_atendente()
        if opcao == "1":
            mensagem = atendente_criar_reserva()
            enviar_mensagem(mensagem)
        elif opcao == "2":
            mensagem = atendente_cancelar_reserva()
            enviar_mensagem(mensagem)
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
