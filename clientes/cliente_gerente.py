import socket

HOST = "localhost"
PORT = 12345

def exibir_menu_gerente():
    print("--- Cliente Gerente ---")
    print("1. Ver reservas por mesa")
    print("2. Ver reservas por período")
    print("3. Ver reservas confirmadas por garçom" )
    print("4. Sair")

    return input("Escolha uma opção:")

def relatorio_por_mesa():
    mesa = int(input("Número da mesa:"))
    return f"GERENTE_RELATORIO_MESA; {mesa}"

def relatorio_por_periodo():
    data_inicio = input("Data de inicio (dd/mm/aaaa):")
    data_fim = input("Data de fim (dd/mm/aaaa):")

    return f"GERENTE_RELATORIO_PERIODO; {data_inicio} ; {data_fim}"

def relatorio_por_garcom():
    garcom_id = input("ID do garçom:")

    return f"GERENTE_RELATORIO_GARCOM; {garcom_id}"

def enviar_mensagem(mensagem):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((HOST, PORT))
            cliente.sendall(mensagem.encode())
            resposta = cliente.recv(1024).decode()
            print(f"\n [RELATORIO]\n {resposta}")

    except ConnectionRefusedError:
        print("Não foi possivel conectar ao servidor.")

def main():
    while True:
        opcao = exibir_menu_gerente()
        if opcao == "1":
            mensagem = relatorio_por_mesa()
            enviar_mensagem(mensagem)
        elif opcao == 2:
            mensagem = relatorio_por_periodo()
            enviar_mensagem(mensagem)
        elif opcao == 3:
            mensagem = relatorio_por_garcom()
            enviar_mensagem(mensagem)
        elif opcao == 4:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()