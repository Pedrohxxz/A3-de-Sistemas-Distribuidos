import socket

from datetime import datetime

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
    try:
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("Data inválida.")
        return "FORMATO_INVÁLIDO"
    
    hora = input("Hora (hh:mm): ")
    print()
    return f"GARCOM_CONFIRMAR;{garcom_id};{numero_mesa};{data_formatada};{hora}"


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
            if mensagem == "Formato_INVÁLIDO":
                print("Formato de data inválido. Tente novamente.")
            else:
                enviar_mensagem(mensagem)
                
        elif opcao == "2":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
