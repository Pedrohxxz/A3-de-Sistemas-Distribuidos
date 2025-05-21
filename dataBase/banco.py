import sqlite3

from datetime import datetime

def formatar_data_iso(data_str):
    try:
        if "/" in data_str:
            return datetime.strptime(data_str, "%d/%m/%Y").strftime("%Y-%m-%d")
        return data_str
    except ValueError:
        return data_str


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
    elif comando == "GERENTE_RELATORIO_PERIODO":
        return relatorio_por_periodo(partes[1], partes[2])
    elif comando == "GERENTE_RELATORIO_GARCOM":
        return relatorio_por_garcom(int(partes[1]))
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
    return "Reserva criada com sucesso.\n"


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
    return "Reserva cancelada com sucesso.\n"


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
    return "Reserva confirmada com sucesso.\n"


def relatorio_por_mesa(numero_mesa):
    conn = sqlite3.connect("banco.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservas WHERE numero_mesa = ?", (numero_mesa,))
    resultados = cursor.fetchall()
    conn.close()

    if not resultados:
        return "Nenhuma reserva encontrada para essa mesa.\n"

    linhas = []
    for r in resultados:
        try:
            data_formatada = datetime.strptime(r[1], '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            data_formatada = r[1]
        linha = f"ID {r[0]} - {data_formatada} {r[2]} - Status: {r[6]}"
        linhas.append(linha)
    resposta = "\n".join(linhas)


    return resposta
    

def relatorio_por_periodo(data_inicio, data_fim):
    # Converte para o formato ISO se ainda estiver em dd/mm/aaaa
    try:
        if "/" in data_inicio:
            data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
        if "/" in data_fim:
            data_fim = datetime.strptime(data_fim, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return "Erro: data inválida."

    conn = sqlite3.connect("banco.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM reservas 
        WHERE data BETWEEN ? AND ?
    """, (data_inicio, data_fim))

    resultados = cursor.fetchall()
    conn.close()

    if not resultados:
        return "Nenhuma reserva encontrada nesse período.\n"

    linhas = []
    for r in resultados:
        try:
            data_formatada = datetime.strptime(r[1], "%Y-%m-%d").strftime('%d/%m/%Y')
        except ValueError:
            data_formatada = r[1]
        linha = f"Mesa {r[3]} - {data_formatada} {r[2]} - Responsável: {r[5]} - Status: {r[6]}"
        linhas.append(linha)

    return "\n".join(linhas)


def relatorio_por_garcom(garcom_id):
    conn = sqlite3.connect("banco.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservas WHERE garcom_id = ?", (garcom_id,))
    resultados = cursor.fetchall()
    conn.close()

    if not resultados:
        return "Nenhuma reserva encontrada para esse garçom.\n"
    
    linhas = []
    for r in resultados:
        try:
            data_formatada = datetime.strptime(r[1], '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            data_formatada = r[1]
        linha = f"Mesa {r[3]} - {data_formatada} {r[2]} - Responsável: {r[5]}"
        linhas.append(linha)
    resposta = "\n".join(linhas)


    return resposta
    
