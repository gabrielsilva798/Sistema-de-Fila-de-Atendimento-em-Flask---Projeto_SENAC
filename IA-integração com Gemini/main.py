import mysql.connector
import pandas as pd
import os

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "senac"),
    "database": os.getenv("MYSQL_DB", "db_movida"),
    "port": int(os.getenv("MYSQL_PORT", 3307))
}

def fetch_pacientes(empresa_id: int) -> pd.DataFrame:
    cnx = mysql.connector.connect(**DB_CONFIG)
    query = """
        SELECT id, cpf, nome, nascimento, telefone, sintomas, classificacao,
               responsavel, empresa_id, entrada_inicio, entrada_fim, criado_em
        FROM pacientes
        WHERE empresa_id = %s
    """
    df = pd.read_sql(query, cnx, params=(empresa_id,))
    cnx.close()
    return df
