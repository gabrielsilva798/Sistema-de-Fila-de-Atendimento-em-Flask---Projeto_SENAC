import os
from mysql.connector import pooling
import pandas as pd

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT"))
}

pool = pooling.MySQLConnectionPool(
    pool_name="movida_pool",
    pool_size=10,
    **DB_CONFIG
)

def get_db():
    """Retorna uma conexão do pool."""
    return pool.get_connection()


#NOVO: Função pronta para Pandas
def query_to_df(query: str, params: tuple = None) -> pd.DataFrame:
    """
    Executa uma query e retorna um Pandas DataFrame.
    Usa conexão do pool automaticamente.
    """
    conn = get_db()
    try:
        df = pd.read_sql(query, conn, params=params)
    finally:
        conn.close()
    return df
