import socket
from datetime import datetime

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
    try:
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("Data inválida.")
        return "FORMATO_INVÁLIDO"
    
    hora = input("Hora (hh:mm): ")
    numero_mesa = int(input("Número da mesa: "))
    quantidade = int(input("Quantidade de pessoas: "))
    nome = input("Nome do responsável: ")
    print()
    return f"ATENDENTE_CRIAR;{data_formatada};{hora};{numero_mesa};{quantidade};{nome}"


def atendente_cancelar_reserva():
    data = input("Data (dd/mm/aaaa): ")
    try:
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("Data inválida.")

        return "FORMATO_INVÁLIDO"
    
    hora = input("Hora (hh:mm): ")
    numero_mesa = input("Número da mesa: ")
    nome = input("Nome do responsável: ")
    print()
    return f"ATENDENTE_CANCELAR;{data_formatada};{hora};{numero_mesa};{nome}"


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
            if mensagem == "FORMATO_INVÁLIDO":
                print("Formato inválido de data inválido.")
            else:
                enviar_mensagem(mensagem)

        elif opcao == "2":
            mensagem = atendente_cancelar_reserva()
            if mensagem == "FORMATO_INVÁLIDO":
                print("Formato inválido de data inválido.")
            else:
                enviar_mensagem(mensagem)
            
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
