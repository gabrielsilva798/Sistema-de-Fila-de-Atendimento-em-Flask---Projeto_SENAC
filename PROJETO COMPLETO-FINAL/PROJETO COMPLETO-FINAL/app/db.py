import os
from mysql.connector import pooling

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "12345678gab"),
    "database": os.getenv("DB_NAME", "db_movida"),
    "port": int(os.getenv("DB_PORT", 3306))
}

pool = pooling.MySQLConnectionPool(pool_name="movida_pool", pool_size=10, **DB_CONFIG)

def get_db():
    return pool.get_connection()
