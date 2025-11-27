import mysql.connector
from flask_login import UserMixin

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678gab",
        database="db_movida"
    )

class Usuario(UserMixin):
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email

def carregar_usuario(user_id):
    db = conectar()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_clientes WHERE id = %s", (user_id,))
    dados = cursor.fetchone()

    if dados:
        return Usuario(id=dados["id"], nome=dados["nome"], email=dados["email"])
    return None