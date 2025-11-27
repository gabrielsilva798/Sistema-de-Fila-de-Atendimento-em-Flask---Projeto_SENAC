import datetime
from .db import get_db

# ---------------------------------------------
# INSERIR PACIENTE
# ---------------------------------------------
def inserir_paciente(data):
    db = get_db()
    cursor = db.cursor()

    sql = """
        INSERT INTO pacientes
        (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (
        data.get("cpf"),
        data.get("nome"),
        data.get("nascimento") or None,
        data.get("telefone"),
        data.get("sintomas"),
        data.get("classificacao"),
        data.get("responsavel")
    ))

    paciente_id = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()
    return paciente_id


# ---------------------------------------------
# INSERIR NA FILA (COM PRIORIDADE)
# ---------------------------------------------
def inserir_na_fila(paciente_id, classificacao):
    db = get_db()
    cursor = db.cursor()

    prioridade = {
        "vermelho": 1,
        "laranja": 2,
        "amarelo": 3,
        "verde": 4
    }.get(classificacao, 4)

    sql = """
        INSERT INTO fila (paciente_id, prioridade, chamado, chegada)
        VALUES (%s, %s, FALSE, NOW())
    """

    cursor.execute(sql, (paciente_id, prioridade))
    db.commit()
    cursor.close()
    db.close()


# ---------------------------------------------
# BUSCAR FILA ATUAL (ordenada por prioridade, retorna dicts)
# ---------------------------------------------
def obter_fila():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    sql = """
        SELECT f.id, p.nome, p.classificacao, f.chamado, f.chegada
        FROM fila f
        JOIN pacientes p ON p.id = f.paciente_id
        WHERE f.chamado = FALSE
        ORDER BY f.prioridade ASC, f.chegada ASC
    """
    cursor.execute(sql)
    dados = cursor.fetchall()

    # converter datetimes para string para JSON
    for item in dados:
        if item.get("chegada") is not None:
            if isinstance(item["chegada"], (datetime.datetime, datetime.date)):
                item["chegada"] = item["chegada"].strftime("%Y-%m-%d %H:%M:%S")
    cursor.close()
    db.close()
    return dados


# ---------------------------------------------
# BUSCAR ÚLTIMOS 5 CHAMADOS (para lista 'últimos')
# ---------------------------------------------
def obter_ultimos():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    sql = """
        SELECT p.nome, f.chegada
        FROM fila f
        JOIN pacientes p ON p.id = f.paciente_id
        WHERE f.chamado = TRUE
        ORDER BY f.chegada DESC
        LIMIT 5
    """
    cursor.execute(sql)
    dados = cursor.fetchall()

    for item in dados:
        if item.get("chegada") is not None:
            if isinstance(item["chegada"], (datetime.datetime, datetime.date)):
                item["chegada"] = item["chegada"].strftime("%Y-%m-%d %H:%M:%S")
    cursor.close()
    db.close()
    return dados
