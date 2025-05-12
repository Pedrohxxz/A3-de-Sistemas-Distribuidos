import socket

HOST = "localhost"
PORT = 12345


def exibir_menu_garcom():
    print("--- Cliente Garçom ---")
    print("1. Confirmar Reserva")
    print("2. Sair")
    return input("Escolha uma opção: ")


def garcom_confirmar_reserva():
    garcom_id = int(input("ID do garçom: "))
    numero_mesa = int(input("Número da mesa: "))
    data = input("Data (dd/mm/aaaa): ")
    hora = input("Hora (hh:mm): ")
    return f"GARCOM_CONFIRMAR;{garcom_id};{numero_mesa};{data};{hora}"


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
        opcao = exibir_menu_garcom()
        if opcao == "1":
            mensagem = garcom_confirmar_reserva()
            enviar_mensagem(mensagem)
        elif opcao == "2":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
