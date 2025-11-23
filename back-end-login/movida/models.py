# arquivo de conexão com MySQL (mantive sua função igual)
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678gab",
        database="db_movida"
    )
