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
    elif comando == "ATENDENTE_CANCELAR":
        return cancelar_reserva(*partes[1:])
    elif comando == "GARCOM_CONFIRMAR":
        return confirmar_reserva(
            (int(partes[1])), (int(partes[2])), (partes[3]), (partes[4])
        )
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


def cancelar_reserva(data, hora, numero_mesa, nome):
    conn = sqlite3.connect("banco.sqlite")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM reservas 
        WHERE data = ? AND hora = ? AND numero_mesa = ? AND nome_responsavel = ? AND status = 'reservado'
    """,
        (data, hora, numero_mesa, nome),
    )
    reserva = cursor.fetchone()

    if not reserva:
        conn.close()
        return "Erro: reserva não encontrada para cancelamento."

    cursor.execute("DELETE FROM reservas WHERE id = ?", (reserva[0],))
    conn.commit()
    conn.close()
    return "Reserva cancelada com sucesso."


def confirmar_reserva(garcom_id, numero_mesa, data, hora):
    conn = sqlite3.connect("banco.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM reservas WHERE numero_mesa = ?  AND data = ? AND hora = ? AND status = 'reservado'",
        (numero_mesa, data, hora),
    )
    reserva = cursor.fetchone()
    if not reserva:
        conn.close()
        return "Erro: Nenhuma reserva ativa encontrada para essa mesa."

    cursor.execute(
        "UPDATE reservas SET status = 'confirmado', garcom_id = ?  WHERE id = ?",
        (garcom_id, reserva[0]),
    )
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
