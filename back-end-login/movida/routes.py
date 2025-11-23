from flask import render_template, request, redirect, session, flash
from .models import conectar

def init_routes(app):

    # Aqui pode ser a LandiPage
    @app.route("/")
    def index():
        return render_template("page.html")

    #------------------------------------------------CADASTRO PACIENTE-------------------------------------------------------------
    @app.route("/cadastro_paciente")
    def cadastrar_paciente():
        return render_template("cadastro_paciente.html")

    # rota para cadatrar pacientes
    @app.route("/registrar_paciente", methods=["POST"])
    def registrar_paciente():

        nome_paciente = request.form["nome_form"]
        email_paciente = request.form["email_form"]
        nascimento_paciente = request.form["nascimento_form"]
        cpf_paciente = request.form["cpf_form"]
        rg_paciente = request.form["rg_form"]
        senha_paciente = request.form["senha_form"]
        confirma_paciente = request.form["confi_senha_form"]

        if senha_paciente != confirma_paciente:
            flash("As senhas não coincidem!")
            return redirect("/")

        try:
            db = conectar()
            cursor = db.cursor()

            sql = """
                INSERT INTO tb_clientes 
                (nome, email, nascimento, cpf, rg, senha)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            valores = (nome_paciente, email_paciente, nascimento_paciente, cpf_paciente, rg_paciente, senha_paciente)

            cursor.execute(sql, valores)
            db.commit()

            flash("Cadastro realizado com sucesso!")
            return redirect("/")

        except Exception as e:
            print("Erro:", e)
            flash("Erro ao cadastrar!")
            return redirect("/")

    # rota de login do paciente
    @app.route("/login_paciente", methods=["POST"])
    def login_paciente():

        email_paciente = request.form["email-login"]
        senha_paciente = request.form["senha-login"]

        try:
            db = conectar()
            cursor = db.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM tb_clientes
                WHERE email = %s AND senha = %s
            """, (email_paciente, senha_paciente))

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

    #----------------------------------------------ESTABELECIMENTO ROTAS--------------------------------------------------
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
                estado_empresa, senha_empresa, confirma_empresa, descricao_empresa
            )

            cursor.execute(sql, valores)
            db.commit()

            flash("Empresa cadastrada com sucesso!")
            return redirect("/")

        except Exception as e:
            print("Erro:", e)
            flash("Erro ao cadastrar a empresa!")
            return redirect("/")

