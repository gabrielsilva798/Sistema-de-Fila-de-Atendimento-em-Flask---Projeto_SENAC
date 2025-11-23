from flask import render_template, request, redirect, session, flash
from flask_login import login_required, login_user, logout_user, current_user
from .models import conectar, Usuario
from movida import bcrypt


def init_routes(app):

    @app.route("/")
    def index():
        return render_template("page.html")

# ---------------- CADASTRO DE PACIENTE -----------------------
    @app.route("/cadastro_paciente")
    def cadastrar_paciente():
        return render_template("cadastro_paciente.html")

    @app.route("/registrar_paciente", methods=["POST"])
    def registrar_paciente():

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

        senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")

        try:
            db = conectar()
            cursor = db.cursor()

            sql = """
                INSERT INTO tb_clientes 
                (nome, email, nascimento, cpf, rg, senha)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            valores = (nome, email, nascimento, cpf, rg, senha_hash)

            cursor.execute(sql, valores)
            db.commit()

            flash("Cadastro realizado com sucesso!")
            return redirect("/")

        except Exception as e:
            print("Erro:", e)
            flash("Erro ao cadastrar!")
            return redirect("/")

# ------------------------ LOGIN PACIENTE ------------------------
    @app.route("/login_paciente", methods=["POST"])
    def login_paciente():

        email = request.form["email-login"]
        senha = request.form["senha-login"]

        try:
            db = conectar()
            cursor = db.cursor(dictionary=True)

            cursor.execute("SELECT * FROM tb_clientes WHERE email = %s", (email,))
            usuario = cursor.fetchone()

            if usuario and bcrypt.check_password_hash(usuario["senha"], senha):

                user_obj = Usuario(
                    id=usuario["id"],
                    nome=usuario["nome"],
                    email=usuario["email"]
                )

                login_user(user_obj)

                flash(f"Bem-vindo, {usuario['nome']}!")
                return redirect("/dashboard")

            flash("E-mail ou senha incorretos")
            return redirect("/")

        except Exception as e:
            print("Erro:", e)
            flash("Erro ao realizar login")
            return redirect("/")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return f"Área protegida! Usuário logado: {current_user.nome}"

# ---------------------------- LOGOUT: nem existe, mas a rota tá aí ------------------------------
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Você saiu da sua conta.")
        return redirect("/")

# ------------------ CADASTRO DE EMPRESA --------------------------
    @app.route("/cadastro_empresa")
    def cadastrar_empresa():
        return render_template("cadastro_empresa.html")

    @app.route("/registrar_empresa", methods=["POST"])
    def registrar_empresa():

        nome_empresa = request.form["nome"]
        cnpj_empresa = request.form["cnpj"]
        segmento_empresa = request.form["segmento"]
        funcionarios_empresa = request.form.get("funcionarios")
        site_empresa = request.form.get("site")
        logo_file = request.files.get("logo")
        logo_empresa = logo_file.read() if logo_file and logo_file.filename != "" else None
        email_empresa = request.form["email"]
        telefone_empresa = request.form["telefone"]
        cep_empresa = request.form["cep"]
        endereco_empresa = request.form["endereco"]
        cidade_empresa = request.form["cidade"]
        estado_empresa = request.form["estado"]
        senha_empresa = request.form["senha"]
        confirma_empresa = request.form["confi_senha"]
        descricao_empresa = request.form.get("descricao")

        if senha_empresa != confirma_empresa:
            flash("As senhas não coincidem!")
            return redirect("/")

        senha_hash = bcrypt.generate_password_hash(senha_empresa).decode("utf-8")

        try:
            db = conectar()
            cursor = db.cursor()

            sql = """
                INSERT INTO tb_empresa
                (nome, cnpj, segmento, funcionarios, site, logo,
                email, telefone, cep, endereco, cidade, estado,
                senha, confirmar_senha, descricao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = (
                nome_empresa, cnpj_empresa, segmento_empresa,
                funcionarios_empresa, site_empresa,
                logo_empresa, email_empresa, telefone_empresa,
                cep_empresa, endereco_empresa, cidade_empresa,
                estado_empresa, senha_hash, senha_hash, descricao_empresa
            )

            cursor.execute(sql, valores)
            db.commit()

            flash("Empresa cadastrada com sucesso!")
            return redirect("/")

        except Exception as e:
            print("Erro:", e)
            flash("Erro ao cadastrar a empresa!")
            return redirect("/")
