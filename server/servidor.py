import socket
import threading
from dataBase.banco import processar_requisicao, inicializar_banco

HOST = 'localhost'  #se quiser colocar seu ip ou o ip de outro computador, coloque aqui!
PORT = 12345 #ATENÇÃO: O número da porta deve ser o mesmo em todos os clientes(gerente, garçom e atendente). E isso vale para o HOST também!

def lidar_com_cliente(conn, addr):
    print(f"[NOVA CONEXÃO] Conectado com {addr}")
    with conn:
        while True:
            dados = conn.recv(1024).decode()
            if not dados:
                break
            print(f"[REQUISIÇÃO] {dados}")
            resposta = processar_requisicao(dados)
            conn.sendall(resposta.encode())

def iniciar_servidor():
    print("[INICIANDO] Servidor está sendo iniciado...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((HOST, PORT))
        servidor.listen()
        print(f"[ESPERANDO] Servidor escutando em {HOST}:{PORT}")
        while True:
            conn, addr = servidor.accept()
            thread = threading.Thread(target=lidar_com_cliente, args=(conn, addr))
            thread.start()
            print(f"[ATIVAS] Conexões ativas: {threading.active_count() - 1}")

if __name__ == "__main__":
    inicializar_banco()
    iniciar_servidor()