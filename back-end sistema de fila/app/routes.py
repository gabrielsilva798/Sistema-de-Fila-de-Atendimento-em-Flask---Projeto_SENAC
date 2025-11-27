from flask import render_template, request, redirect
from .models import inserir_paciente, inserir_na_fila, obter_fila, obter_ultimos

def init_routes(app, socketio):

    @app.route("/")
    def home():
        return render_template("cadastro.html")

    @app.route("/cadastro", methods=["POST"])
    def cadastro():
        dados = {
            "cpf": request.form.get("cpf"),
            "nome": request.form.get("nome"),
            "nascimento": request.form.get("nascimento"),
            "telefone": request.form.get("telefone"),
            "sintomas": request.form.get("sintomas"),
            "classificacao": request.form.get("classificacao"),
            "responsavel": request.form.get("responsavel"),
        }

        paciente_id = inserir_paciente(dados)
        inserir_na_fila(paciente_id, dados["classificacao"])

        fila = obter_fila()
        # emitir para clientes (não usar broadcast param em versões recentes)
        socketio.emit("fila_atualizada", {"fila": fila})

        return redirect("/fila")

    @app.route("/fila")
    def fila():
        return render_template(
            "fila.html",
            fila=obter_fila(),
            ultimos=obter_ultimos()
        )
