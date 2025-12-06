from flask import render_template, request, redirect, url_for, session, flash, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.db import get_db
import app.models as models
import pandas as pd
import matplotlib.pyplot as plt
from functools import wraps
import os
import io
import json
from dotenv import load_dotenv
from app.utils.gemini_ai import gemini_instrucao_segura
from app.utils.pandas_ops import executar_operacao

# carregar variáveis .env
load_dotenv()

# configurar chave da API
#Decorato de login
def login_required_empresa(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "empresa_id" not in session:
            flash("Você precisa estar logado para acessar essa página.", "warning")
            return redirect(url_for("login_estabelecimento"))
        return f(*args, **kwargs)
    return wrapper


# register_routes(app, socketio)
def register_routes(app, socketio):
    @app.route('/')
    def index():
        return render_template('index.html')

    # REGISTRAR EMPRESA
    @app.route('/registrar_empresa', methods=['GET', 'POST'])
    def registrar_empresa():
        if request.method == 'GET':
            return render_template('cadastro_empresa.html')

        senha = request.form.get('senha', '')
        confirmar = request.form.get('confirmar_senha', '') or senha

        if not senha or senha != confirmar:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('registrar_empresa'))

        data = {
            'nome': request.form.get('nome'),
            'cnpj': request.form.get('cnpj'),
            'segmento': request.form.get('segmento'),
            'funcionarios': request.form.get('funcionarios') or None,
            'site': request.form.get('site'),
            'email': request.form.get('email'),
            'telefone': request.form.get('telefone'),
            'cep': request.form.get('cep'),
            'endereco': request.form.get('endereco'),
            'cidade': request.form.get('cidade'),
            'estado': request.form.get('estado'),
            'senha': generate_password_hash(senha),
            'confirmar_senha': generate_password_hash(confirmar),
            'descricao': request.form.get('descricao')
        }

        try:
            models.create_empresa(data)
        except Exception as e:
            print("Erro criando empresa:", e)
            flash('Erro ao registrar empresa (ver logs).', 'danger')
            return redirect(url_for('registrar_empresa'))

        flash('Empresa registrada com sucesso. Faça login.', 'success')
        return redirect(url_for('login_estabelecimento'))

    # --------------------
    # LOGIN EMPRESA
    # --------------------
    @app.route('/login_estabelecimento', methods=['GET'])
    def login_estabelecimento():
        return render_template('login-estabelecimento.html')

    @app.route('/login_empresa', methods=['POST'])
    def login_empresa():
        email = request.form.get('email')
        senha = request.form.get('senha')

        empresa = models.get_empresa_by_email(email)
        if not empresa or not check_password_hash(empresa.get('senha', ''), senha):
            flash('E-mail ou senha incorretos', 'danger')
            return redirect(url_for('login_estabelecimento'))

        session['empresa_id'] = empresa['id']
        session['empresa_nome'] = empresa['nome']
        return redirect(url_for('tela_principal_estabelecimento'))

    # --------------------
    # LOGOUT (aliases)
    # --------------------
    def _do_logout():
        empresa_id = session.get('empresa_id')
        if empresa_id:
            try:
                models.limpar_fila_empresa(empresa_id)
            except Exception as e:
                print("Erro ao limpar fila no logout:", e)
            try:
                socketio.emit('update_fila', {'empresa_id': empresa_id}, broadcast=True)
            except Exception:
                pass
        session.clear()

    @app.route('/logout', endpoint='logout_estabelecimento')
    @app.route('/logout_estabelecimento')
    def logout():
        _do_logout()
        return redirect(url_for('index'))

    # --------------------
    # CLIENTE (PACIENTE): LOGIN / CADASTRO
    # --------------------
    @app.route('/login_cadastro_paciente', methods=['GET'])
    def login_cadastro_paciente():
        return render_template('login-cadastro-paciente.html')

    @app.route('/registrar_cliente', methods=['POST'])
    def registrar_cliente():
        senha = request.form.get('senha_form', '').strip()
        confirmar = request.form.get('confi_senha_form', '').strip()

        # VALIDAÇÕES
        if not senha:
            flash('Informe uma senha.', 'warning')
            return redirect(url_for('login_cadastro_paciente'))

        if senha != confirmar:
            flash('Senhas não conferem.', 'danger')
            return redirect(url_for('login_cadastro_paciente'))

        if len(senha) < 8:
            flash('A senha deve ter no mínimo 8 caracteres.', 'warning')
            return redirect(url_for('login_cadastro_paciente'))

        data = {
            'nome': request.form.get('nome_form'),
            'email': request.form.get('email_form'),
            'nascimento': request.form.get('nascimento_form'),
            'cpf': request.form.get('cpf_form'),
            'rg': request.form.get('rg_form'),
            'senha': generate_password_hash(senha)
        }

        try:
            models.create_cliente(data)
        except Exception as e:
            print("Erro ao criar cliente:", e)
            flash('Erro ao criar conta (ver logs).', 'danger')
            return redirect(url_for('login_cadastro_paciente'))

        flash('Conta criada. Faça login.', 'success')
        return redirect(url_for('login_cadastro_paciente'))

    @app.route('/login_cliente', methods=['POST'])
    def login_cliente():
        email = request.form.get('email-login')
        senha = request.form.get('senha-login')

        cliente = models.get_cliente_by_email(email)
        if not cliente or not check_password_hash(cliente.get('senha', ''), senha):
            flash('E-mail ou senha incorretos', 'danger')
            return redirect(url_for('login_cadastro_paciente'))

        session['cliente_id'] = cliente['id']
        session['cliente_nome'] = cliente['nome']
        session['cliente_cpf'] = cliente['cpf']

        return redirect(url_for('fila_paciente'))
    
    @app.route('/logout_cliente')
    def logout_cliente():
        # limpa apenas dados do paciente
        session.pop('cliente_id', None)
        session.pop('cliente_nome', None)
        session.pop('cliente_cpf', None)

        flash('Você saiu da sua conta.', 'success')
        return redirect(url_for('index'))


    # --------------------
    # FILA DO PACIENTE (visualizar posição)
    # --------------------
    @app.route('/fila')
    def fila_paciente():
        if 'cliente_id' not in session:
            return redirect(url_for('login_cadastro_paciente'))

        conn = None
        cur = None
        try:
            conn = get_db()
            cur = conn.cursor(dictionary=True)

            cur.execute("""
                SELECT p.*, t.nome as empresa_nome
                FROM pacientes p
                JOIN tb_empresa t ON p.empresa_id = t.id
                WHERE p.cpf = %s
                ORDER BY p.entrada_inicio DESC
            """, (session.get('cliente_cpf'),))

            registros = cur.fetchall()
            if not registros:
                return render_template('fila.html',
                                       paciente_nome=session.get('cliente_nome'),
                                       empresa_nome='-',
                                       posicao='-',
                                       paciente_id='-',
                                       paciente_classificacao='-',
                                       tempo_medio='-',
                                       ultimos=[])

            reg = registros[0]

            cur.execute("""
                SELECT f.id AS fila_id, f.chegada
                FROM fila f
                WHERE f.paciente_id = %s AND f.empresa_id = %s
                ORDER BY f.chegada ASC
                LIMIT 1
            """, (reg['id'], reg['empresa_id']))
            fila_row = cur.fetchone()

            if not fila_row:
                return render_template('fila.html',
                                       paciente_nome=reg.get('nome'),
                                       empresa_nome=reg.get('empresa_nome'),
                                       posicao='-',
                                       paciente_id=reg.get('id'),
                                       paciente_classificacao=reg.get('classificacao') or '-',
                                       tempo_medio='-',
                                       ultimos=[])

            chegada = fila_row['chegada']
            cur.execute("""
                SELECT COUNT(*) AS pos
                FROM fila
                WHERE empresa_id=%s AND chamado=FALSE AND chegada <= %s
            """, (reg['empresa_id'], chegada))
            cnt = cur.fetchone()
            pos = cnt['pos'] if cnt and cnt.get('pos') is not None else 0

            cur.execute("""
                SELECT AVG(TIMESTAMPDIFF(MINUTE, inicio_atendimento, fim_atendimento)) as media_min
                FROM em_atendimento
                WHERE empresa_id=%s AND fim_atendimento IS NOT NULL
            """, (reg['empresa_id'],))
            avg_row = cur.fetchone()
            tempo_medio = '-'
            if avg_row and avg_row.get('media_min') is not None:
                media_min = float(avg_row['media_min'])
                if media_min < 60:
                    tempo_medio = f"{int(media_min)} min"
                else:
                    horas = int(media_min // 60)
                    minutos = int(media_min % 60)
                    tempo_medio = f"{horas}h {minutos}m"

            cur.execute("""
                SELECT nome, classificacao, fim_atendimento AS saida
                FROM em_atendimento
                WHERE empresa_id=%s AND fim_atendimento IS NOT NULL
                ORDER BY fim_atendimento DESC
                LIMIT 5
            """, (reg['empresa_id'],))
            ult = cur.fetchall()
            ult_list = []
            for u in ult:
                saida = u.get('saida')
                if isinstance(saida, (datetime,)):
                    saida_str = saida.strftime('%H:%M')
                else:
                    saida_str = str(saida) if u.get('saida') else '-'
                ult_list.append({'nome': u.get('nome'), 'classificacao': u.get('classificacao'), 'saida': saida_str})

            return render_template('fila.html',
                                   paciente_nome=reg.get('nome'),
                                   empresa_nome=reg.get('empresa_nome'),
                                   posicao=pos,
                                   paciente_id=reg.get('id'),
                                   paciente_classificacao=reg.get('classificacao') or '-',
                                   tempo_medio=tempo_medio,
                                   ultimos=ult_list)
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    #------------------------------------
    #4 Primeiros da Fila Geral
    #--------------------------------
    @app.route('/api/primeiros_fila')
    def api_primeiros_fila():
        empresa_id = session.get('empresa_id')
        if not empresa_id:
            return jsonify([])

        conn = get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT p.nome, p.classificacao, f.chegada
            FROM fila f
            JOIN pacientes p ON p.id = f.paciente_id
            WHERE f.empresa_id=%s AND f.chamado=FALSE
            ORDER BY f.chegada ASC
            LIMIT 4
        """, (empresa_id,))

        dados = cur.fetchall() or []

        # adiciona posição
        for idx, p in enumerate(dados, start=1):
            p["posicao"] = idx

        cur.close()
        conn.close()

        return jsonify(dados)

    #------------------------------
    #4 Últimos Pacientes em Atendimento
    #------------------------------
    @app.route('/api/em_atendimento')
    def api_em_atendimento():
        empresa_id = session.get('empresa_id')
        if not empresa_id:
            return jsonify([])

        conn = get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT 
                nome,
                classificacao,
                DATE_FORMAT(inicio_atendimento, '%H:%M') AS inicio
            FROM em_atendimento
            WHERE empresa_id=%s AND fim_atendimento IS NULL
            ORDER BY inicio_atendimento ASC
            LIMIT 4
        """, (empresa_id,))

        dados = cur.fetchall() or []

        cur.close()
        conn.close()

        return jsonify(dados)


    # ------------------------------
    # WEBSOCKET - FILA EM TEMPO REAL
    # ------------------------------

    from flask_socketio import emit, join_room
    import time
    from threading import Thread

    # ---------- Função que recalcula toda a fila ----------
    def calcular_fila(cliente_cpf):
        conn = get_db()
        cur = conn.cursor(dictionary=True)

        # Localiza paciente
        cur.execute("""
            SELECT p.*, t.nome as empresa_nome
            FROM pacientes p
            JOIN tb_empresa t ON p.empresa_id = t.id
            WHERE p.cpf = %s
            ORDER BY p.entrada_inicio DESC
        """, (cliente_cpf,))
        registros = cur.fetchall()

        if not registros:
            cur.close(); conn.close()
            return None

        reg = registros[0]

        # Posição na fila
        cur.execute("""
            SELECT f.id AS fila_id, f.chegada
            FROM fila f
            WHERE f.paciente_id = %s AND f.empresa_id = %s
            ORDER BY f.chegada ASC
            LIMIT 1
        """, (reg['id'], reg['empresa_id']))
        fila_row = cur.fetchone()

        if not fila_row:
            cur.close(); conn.close()
            return {
                "paciente_nome": reg["nome"],
                "empresa_nome": reg["empresa_nome"],
                "posicao": "-",
                "classificacao": reg.get("classificacao") or "-",
                "tempo_medio": "-",
                "ultimos": []
            }

        # Calcular posição
        chegada = fila_row['chegada']
        cur.execute("""
            SELECT COUNT(*) AS pos
            FROM fila
            WHERE empresa_id=%s AND chamado=FALSE AND chegada <= %s
        """, (reg['empresa_id'], chegada))
        pos = cur.fetchone()["pos"]

        # Tempo médio
        cur.execute("""
            SELECT AVG(TIMESTAMPDIFF(MINUTE, inicio_atendimento, fim_atendimento)) as media_min
            FROM em_atendimento
            WHERE empresa_id=%s AND fim_atendimento IS NOT NULL
        """, (reg['empresa_id'],))
        avg = cur.fetchone()["media_min"]

        tempo_medio = "-"
        if avg is not None:
            avg = float(avg)
            tempo_medio = f"{int(avg)} min" if avg < 60 else f"{int(avg//60)}h {int(avg%60)}m"

        # Últimos 5
        cur.execute("""
            SELECT nome, classificacao, fim_atendimento AS saida
            FROM em_atendimento
            WHERE empresa_id=%s AND fim_atendimento IS NOT NULL
            ORDER BY fim_atendimento DESC
            LIMIT 5
        """, (reg['empresa_id'],))
        ult = cur.fetchall()

        ult_formatado = []
        for u in ult:
            saida = u["saida"]
            if isinstance(saida, datetime):
                saida = saida.strftime("%H:%M")
            ult_formatado.append({
                "nome": u["nome"],
                "classificacao": u["classificacao"],
                "saida": saida if saida else "-"
            })

        cur.close()
        conn.close()

        return {
            "paciente_nome": reg["nome"],
            "empresa_nome": reg["empresa_nome"],
            "posicao": pos,
            "classificacao": reg.get("classificacao") or "-",
            "tempo_medio": tempo_medio,
            "ultimos": ult_formatado
        }

    # -------- Thread que envia atualização contínua --------
    def worker_fila(cliente_cpf, room):
        while True:
            dados = calcular_fila(cliente_cpf)
            socketio.emit("fila_update", dados, room=room, namespace="/fila")
            time.sleep(3)  # atualização a cada 3s

    # ----- Evento WebSocket: paciente conectou -----
    @socketio.on("connect", namespace="/fila")
    def ws_connect():
        print("Paciente conectou:", request.sid)

    # ----- Evento WebSocket: paciente entrou na fila -----
    @socketio.on("join_fila", namespace="/fila")
    def join_fila(data):
        cpf = data.get("cpf")
        room = request.sid
        join_room(room)

        # Inicia thread individual para esse paciente
        thread = Thread(target=worker_fila, args=(cpf, room))
        thread.daemon = True
        thread.start()

        emit("status", {"msg": "Monitorando fila..."})


    # --------------------
    # PAINEL ESTABELECIMENTO
    # --------------------
    @app.route('/tela-principal-estabelecimento')
    def tela_principal_estabelecimento():
        if 'empresa_id' not in session:
            return redirect(url_for('login_estabelecimento'))

        empresa_id = session['empresa_id']
        try:
            em = models.obter_em_atendimento(empresa_id)
        except Exception as e:
            print("Erro ao obter em_atendimento:", e)
            em = []

        return render_template(
            'tela-principal-estabelecimento.html',
            clinic_name=session.get('empresa_nome'),
            em_atendimento=em
        )

    # --------------------
    # CADASTRAR PACIENTE (ESTABELECIMENTO)
    # --------------------
    @app.route('/cadastrar-paciente', methods=['GET'])
    def view_cadastrar_paciente():
        if 'empresa_id' not in session:
            return redirect(url_for('login_estabelecimento'))
        return render_template('cadastrar-paciente.html', clinic_name=session.get('empresa_nome'))

    @app.route('/cadastrar-paciente', methods=['GET'], endpoint='cadastrar_paciente')
    def cadastrar_paciente_alias():
        if 'empresa_id' not in session:
            return redirect(url_for('login_estabelecimento'))
        return render_template('cadastrar-paciente.html', clinic_name=session.get('empresa_nome'))

    @app.route('/cadastro', methods=['POST'])
    def action_cadastro():
        if 'empresa_id' not in session:
            return redirect(url_for('login_estabelecimento'))

        empresa_id = session['empresa_id']

        data = {
            'cpf': request.form.get('cpf'),
            'nome': request.form.get('nome'),
            'nascimento': request.form.get('nascimento'),
            'telefone': request.form.get('telefone'),
            'sintomas': request.form.get('sintomas'),
            'classificacao': request.form.get('classificacao'),
            'responsavel': request.form.get('responsavel') or session.get('empresa_nome')
        }

        try:
            res = models.inserir_paciente_empresa(data, empresa_id)
        except Exception as e:
            print("Erro ao inserir paciente:", e)
            flash('Erro ao inserir paciente (ver logs).', 'danger')
            return redirect(url_for('view_cadastrar_paciente'))

        try:
            socketio.emit('update_fila', {'empresa_id': empresa_id}, broadcast=True)
            try:
                socketio.emit('atualizar_fila_paciente', {'paciente_id': res.get('paciente_id'), 'posicao': None}, broadcast=True)
            except Exception:
                pass
        except Exception:
            pass

        flash('Paciente inserido na fila', 'success')
        return redirect(url_for('view_cadastrar_paciente'))

    # --------------------
    # LISTA DE PACIENTES NA FILA
    # --------------------
    @app.route('/lista-pacientes')
    def lista_pacientes():
        if 'empresa_id' not in session:
            return redirect(url_for('login_estabelecimento'))

        empresa_id = session['empresa_id']
        try:
            fila = models.obter_fila_empresa(empresa_id)
        except Exception as e:
            print("Erro obter fila:", e)
            fila = []

        return render_template(
            'lista-pacientes.html',
            clinic_name=session.get('empresa_nome'),
            fila=fila
        )

    # --------------------
    # INICIAR ATENDIMENTO
    # --------------------
    @app.route('/iniciar_atendimento/<int:fila_id>', methods=['POST'])
    def iniciar_atendimento_route(fila_id):
        empresa_id = session.get('empresa_id')
        res = models.iniciar_atendimento(fila_id, empresa_id)

        if res.get('ok'):
            try:
                socketio.emit('update_fila', {'empresa_id': empresa_id}, broadcast=True)
            except Exception:
                pass

            try:
                conn = get_db(); cur = conn.cursor(dictionary=True)
                cur.execute("""
                    SELECT nome, classificacao, fim_atendimento AS saida
                    FROM em_atendimento
                    WHERE empresa_id=%s AND fim_atendimento IS NOT NULL
                    ORDER BY fim_atendimento DESC
                    LIMIT 5
                """, (empresa_id,))
                ult = cur.fetchall()
                ult_list = []
                for u in ult:
                    saida = u.get('saida')
                    if hasattr(saida, 'strftime'):
                        saida_str = saida.strftime('%H:%M')
                    else:
                        saida_str = str(saida) if saida else '-'
                    ult_list.append({'nome': u.get('nome'), 'classificacao': u.get('classificacao'), 'saida': saida_str})
                cur.close(); conn.close()
                socketio.emit('atualizar_ultimos', ult_list, broadcast=True)
            except Exception:
                pass

            flash('Atendimento iniciado', 'success')
        else:
            flash('Erro ao iniciar atendimento', 'danger')

        return redirect(url_for('lista_pacientes'))

    # --------------------
    # REMOVER DO ATENDIMENTO
    # --------------------
    @app.route('/remover_em_atendimento/<int:em_id>', methods=['POST'])
    def remover_em_atendimento_route(em_id):
        empresa_id = session.get('empresa_id')

        try:
            models.remover_em_atendimento(em_id)
        except Exception as e:
            print("Erro remover em_atendimento:", e)

        try:
            socketio.emit('update_fila', {'empresa_id': empresa_id}, broadcast=True)
        except Exception:
            pass

        flash('Paciente removido do atendimento', 'success')
        return redirect(url_for('tela_principal_estabelecimento'))

    # --------------------
    # CONFIGURAÇÕES / EXCLUIR CONTA
    # --------------------
    @app.route('/configuracoes-estabelecimento', methods=['GET', 'POST'])
    @app.route('/config_empresa', methods=['GET', 'POST'], endpoint='config_empresa')
    def configuracoes_estabelecimento():
        if 'empresa_id' not in session:
            return redirect(url_for('login_estabelecimento'))

        if request.method == 'POST':
            novo = request.form.get('nome_clinica')

            if novo:
                conn = None
                cur = None
                try:
                    conn = get_db()
                    cur = conn.cursor()
                    cur.execute("UPDATE tb_empresa SET nome=%s WHERE id=%s", (novo, session['empresa_id']))
                    conn.commit()
                    session['empresa_nome'] = novo
                    flash('Nome atualizado', 'success')
                except Exception as e:
                    print("Erro atualizar nome:", e)
                    flash('Erro ao atualizar nome (ver logs).', 'danger')
                finally:
                    if cur: cur.close()
                    if conn: conn.close()

            return redirect(url_for('config_empresa'))

        return render_template(
            'configuracoes-estabelecimento.html',
            clinic_name=session.get('empresa_nome')
        )

    @app.route('/excluir_conta', methods=['POST'])
    def excluir_conta():
        empresa_id = session.get('empresa_id')

        if empresa_id:
            try:
                models.excluir_conta_empresa(empresa_id)
            except Exception as e:
                print("Erro excluir conta:", e)

            try:
                socketio.emit('update_fila', {'empresa_id': empresa_id}, broadcast=True)
            except Exception:
                pass

        session.clear()
        flash('Conta excluída', 'success')
        return redirect(url_for('index'))
# ------------------------------------------------GEMINI----------------------------------

    #Rota da página do gemini
    @app.route("/gemini")
    @login_required_empresa
    def gemini():
        return render_template("gemini.html")


    #tabela via pandas.
    @app.route("/gemini/tabela", methods=["POST"])
    @login_required_empresa
    def gemini_tabela():
        prompt = request.form.get("prompt", "")
        empresa_id = session.get("empresa_id")

        if not prompt:
            return "<h3>Informe um prompt.</h3>"

        # ====== BANCO ======
        conn = get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT 
                nome,
                nascimento,
                classificacao,
                entrada_inicio
            FROM pacientes
            WHERE empresa_id = %s
            ORDER BY entrada_inicio DESC
            LIMIT 15
        """, (empresa_id,))

        rows = cur.fetchall() or []

        cur.close()
        conn.close()

        df = pd.DataFrame(rows)

        if df.empty:
            return "<h3>Sem dados disponíveis.</h3>"

        # ====== IA (SIMULAÇÃO VIA FUNÇÃO) ======
        instrucao = gemini_instrucao_segura(prompt, df.to_json(orient="records"))

        # ====== EXECUTAR OPERAÇÃO ======
        resultado = executar_operacao(df, instrucao)

        # ====== TABELA HTML ======
        return resultado.to_html(classes="tabela-gemini", index=False)


    # ============================================================
    # 2) ROTA GRÁFICO 
    @app.route("/gemini/grafico", methods=["POST"])
    @login_required_empresa
    def gemini_grafico():
        try:
            empresa_id = request.form.get("empresa_id")
            prompt = request.form.get("prompt")

            # --- exemplo simples de dataframe ---
            data = {
                "classificacao": ["A", "A", "B", "B", "C"],
                "idade": [30, 25, 40, 50, 22]
            }
            df = pd.DataFrame(data)

            # --- gera o gráfico ---
            fig, ax = plt.subplots()
            df["idade"].plot(kind="bar", ax=ax)
            ax.set_title("Exemplo de gráfico")
            ax.set_xlabel("Índice")
            ax.set_ylabel("Idade")

            # --- salvando em buffer ---
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plt.close(fig)

            return Response(img.getvalue(), mimetype="image/png")

        except Exception as e:
            return {"erro": str(e)}, 500

        

    # --------------- SOCKET EVENTS (opcional server-side) ---------------
    # Você pode adicionar handlers socketio aqui, por exemplo:
    # @socketio.on('connect')
    # def on_connect():
    #     print('cliente conectado', request.sid)
    # Fim do registro de rotas