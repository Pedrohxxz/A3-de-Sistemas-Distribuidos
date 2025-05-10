import sqlite3

def inicializar_banco():
    conn = sqlite3.connect("banco.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            hora TEXT,
            numero_mesa INTEGER,
            quantidade_pessoas INTEGER,
            nome_responsavel TEXT,
            status TEXT,
            garcom_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def processar_requisicao(mensagem):
    partes = mensagem.strip().split(';')
    comando = partes[0]

    if comando == "ATENDENTE_CRIAR":
        return criar_reserva(*partes[1:])
    elif comando == "GARCOM_CONFIRMAR":
        return confirmar_reserva(int(partes[1]))
    elif comando == "GERENTE_RELATORIO_MESA":
        return relatorio_por_mesa(int(partes[1]))
    else:
        return "Comando desconhecido."

def criar_reserva(data, hora, numero_mesa, quantidade, nome):
    conn = sqlite3.connect("banco.sqlite")
    cursor = conn.cursor()
    
    # Verifica se já existe uma reserva com essas informações aí data/hora/mesa
    cursor.execute("SELECT * FROM reservas WHERE data = ? AND hora = ? AND numero_mesa = ? AND status = 'reservado'",
                (data, hora, numero_mesa))
    if cursor.fetchone():
        conn.close()
        return "Erro: mesa já reservada nesse horário."
    
    cursor.execute('''
        INSERT INTO reservas (data, hora, numero_mesa, quantidade_pessoas, nome_responsavel, status)
        VALUES (?, ?, ?, ?, ?, 'reservado')
    ''', (data, hora, numero_mesa, quantidade, nome))
    
    conn.commit()
    conn.close()
    return "Reserva criada com sucesso."

def confirmar_reserva(numero_mesa):
    conn = sqlite3.connect("banco.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservas WHERE numero_mesa = ? AND status = 'reservado'", (numero_mesa,))
    reserva = cursor.fetchone()
    if not reserva:
        conn.close()
        return "Erro: nenhuma reserva ativa encontrada para essa mesa."
    
    cursor.execute("UPDATE reservas SET status = 'confirmado' WHERE id = ?", (reserva[0],))
    conn.commit()
    conn.close()
    return "Reserva confirmada com sucesso."

def relatorio_por_mesa(numero_mesa):
    conn = sqlite3.connect("banco.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservas WHERE numero_mesa = ?", (numero_mesa,))
    resultados = cursor.fetchall()
    conn.close()

    if not resultados:
        return "Nenhuma reserva encontrada para essa mesa."

    resposta = "\n".join([f"ID {r[0]} - {r[1]} {r[2]} - Status: {r[6]}" for r in resultados])
    return resposta
