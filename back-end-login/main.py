from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector, os
from dotenv import load_dotenv

app = Flask(__name__)

# colocar essa chave em um .ENV depois
# É OBRIGATÓRIA se você usar session ou flash(pesquisar mais depois).
# Posso usar chave fixa pq é ligada a aplicação, não aos usuários.
app.secret_key = os.getenv("SECRET_KEY_FORM")

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678gab",
        database="db_movida"
    )

# Aqui pode ser a LandiPage
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro")
def cadastrar():
    return render_template("cadastro.html")

# rota para cadatrar usuários
@app.route("/registrar", methods=["POST"])
def registrar():

    nome = request.form["nome_form"]
    email = request.form["email_form"]
    nascimento = request.form["nascimento_form"]
    cpf = request.form["cpf_form"]
    rg = request.form["rg_form"]
    senha = request.form["senha_form"]
    confirma = request.form["confi_senha_form"]

    if senha != confirma:
        flash("As senhas não coincidem!")
        return redirect("/")

    try:
        db = conectar()
        cursor = db.cursor()

        # Não usei .FORMAT pq o carinha falou que isso pode ajudar em SQL Injection.
        sql = """
            INSERT INTO clientes 
            (nome, email, nascimento, cpf, rg, senha)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (nome, email, nascimento, cpf, rg, senha)

        cursor.execute(sql, valores)
        db.commit()

        flash("Cadastro realizado com sucesso!")
        return redirect("/")

    except Exception as e:
        print("Erro:", e)
        flash("Erro ao cadastrar!")
        return redirect("/")


# rota de login
@app.route("/login", methods=["POST"])
def login():

    email = request.form["email-login"]
    senha = request.form["senha-login"]

    try:
        db = conectar()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM clientes
            WHERE email = %s AND senha = %s
        """, (email, senha))

        usuario = cursor.fetchone()

        if usuario:
            session["usuario"] = usuario["nome"]
            return "Login realizado! Bem-vindo, " + usuario["nome"]
        else:
            flash("E-mail ou senha incorretos")
            return redirect("/")

    except Exception as e:
        print(e)
        flash("Erro ao realizar login")
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
