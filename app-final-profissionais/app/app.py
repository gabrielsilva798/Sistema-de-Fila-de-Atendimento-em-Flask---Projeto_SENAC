from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# --- CONFIGURAÇÃO SECRETA (Para sessões e mensagens flash) ---
app.secret_key = '159753486200' 

# --- CONFIGURAÇÃO DO BANCO DE DADOS (MySQL Connector) ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'senac',
    'database': 'clinica_db',
    'port': 3307
}

def get_db_connection():
    """Tenta estabelecer uma conexão com o banco de dados."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def execute_query(query, params=None, fetch_type='all'):
    """Função auxiliar para executar queries (SELECT, INSERT, UPDATE, DELETE)."""
    conn = get_db_connection()
    if not conn:
        return [] if fetch_type in ['all', 'one'] else None # Retorna vazio ou None em caso de falha de conexão

    cursor = conn.cursor(dictionary=True) # Usando dictionary=True para retornar dados como dicionário
    try:
        cursor.execute(query, params)
        
        if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
            conn.commit()
            return cursor.lastrowid if 'INSERT' in query.upper() else True
        
        if fetch_type == 'one':
            return cursor.fetchone()
        else:
            return cursor.fetchall()
            
    except Error as e:
        print(f"Erro ao executar query: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# -------------------------------------------------------------
# ------------------------ ROTAS FLASK ------------------------
# -------------------------------------------------------------

# A. Rota Principal e Filtro (Read/Listar)
@app.route('/profissionais', methods=['GET', 'POST'])
def profissionais():
    
    query_base = "SELECT * FROM profissionais"
    filtros = []
    
    especialidade_selecionada = 'Todas'
    status_selecionado = 'Todos'

    if request.method == 'POST' and request.form.get('acao_form') == 'filtrar':
        especialidade = request.form.get('filtro_especialidade')
        status = request.form.get('filtro_status')

        if especialidade and especialidade != 'Todas':
            filtros.append(f"especialidade = '{especialidade}'")
            especialidade_selecionada = especialidade
            
        if status and status != 'Todos':
            filtros.append(f"status_clinica = '{status}'")
            status_selecionado = status
            
    if filtros:
        query_base += " WHERE " + " AND ".join(filtros)
        
    query_base += " ORDER BY nome_completo"
    
    profissionais_data = execute_query(query_base)

    return render_template('profissionais.html', 
                           profissionais=profissionais_data,
                           especialidade_selecionada=especialidade_selecionada,
                           status_selecionado=status_selecionado)


# B. Rotas de Cadastro (Create)
@app.route('/cadastrar-profissional', methods=['GET', 'POST'])
def cadastrar_profissional():
    if request.method == 'POST':
        dados = request.form
        nome = dados['nome_completo']
        data_nasc = dados['data_nascimento']
        telefone = dados['telefone']
        email = dados['email_profissional']
        especialidade = dados['especialidade']
        registro = dados['registro_crm_coren']
        estado_crm = dados['estado_crm']
        turno = dados['turno_atendimento']
        status = dados['status_clinica']
        info_adicional = dados.get('informacoes_adicionais', '')
        
        sql = """
            INSERT INTO profissionais (nome_completo, data_nascimento, telefone, email_profissional, 
                                       especialidade, registro_crm_coren, estado_crm, 
                                       turno_atendimento, status_clinica, informacoes_adicionais)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (nome, data_nasc, telefone, email, especialidade, 
                  registro, estado_crm, turno, status, info_adicional)
        
        resultado = execute_query(sql, params, fetch_type='insert')
        
        if resultado is not False:
            flash(f'Profissional {nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('profissionais'))
        else:
            flash('Erro ao cadastrar profissional. Verifique se o e-mail ou registro já existe.', 'danger')
            return redirect(url_for('cadastrar_profissional'))

    return render_template('cadastrar-prof.html')


# C. Rotas de Edição (Update)
@app.route('/editar-profissional/<int:id>', methods=['GET', 'POST'])
def editar_profissional(id):
    if request.method == 'POST':
        dados = request.form
        nome = dados['nome_completo']
        data_nasc = dados['data_nascimento']
        telefone = dados['telefone']
        email = dados['email_profissional']
        especialidade = dados['especialidade']
        registro = dados['registro_crm_coren']
        estado_crm = dados['estado_crm']
        turno = dados['turno_atendimento']
        status = dados['status_clinica']
        info_adicional = dados.get('informacoes_adicionais', '')
        
        sql = """
            UPDATE profissionais SET 
                nome_completo = %s, data_nascimento = %s, telefone = %s, email_profissional = %s, 
                especialidade = %s, registro_crm_coren = %s, estado_crm = %s, 
                turno_atendimento = %s, status_clinica = %s, informacoes_adicionais = %s
            WHERE id = %s
        """
        params = (nome, data_nasc, telefone, email, especialidade, 
                  registro, estado_crm, turno, status, info_adicional, id)
                  
        resultado = execute_query(sql, params, fetch_type='update')
        
        if resultado is not False:
            flash(f'Profissional {nome} atualizado com sucesso!', 'success')
            return redirect(url_for('profissionais'))
        else:
            flash('Erro ao editar profissional. Verifique os dados.', 'danger')
            return redirect(url_for('editar_profissional', id=id))
            
    # Rota GET - Carrega os dados para exibição
    sql_select = 'SELECT * FROM profissionais WHERE id = %s'
    profissional = execute_query(sql_select, (id,), fetch_type='one')
    
    if profissional:
        return render_template('editar-prof.html', profissional=profissional)
    else:
        flash('Profissional não encontrado.', 'danger')
        return redirect(url_for('profissionais'))


# D. Rota de Exclusão (Delete)
@app.route('/excluir-profissional', methods=['POST'])
def excluir_profissional():
    if request.method == 'POST':
        id_prof = request.form.get('id')
        
        sql = 'DELETE FROM profissionais WHERE id = %s'
        resultado = execute_query(sql, (id_prof,), fetch_type='delete')
            
        if resultado is not False:
            flash('Profissional excluído com sucesso!', 'success')
        else:
            flash('Erro ao excluir profissional.', 'danger')
            
    return redirect(url_for('profissionais'))

# --- Roda o Servidor ---
if __name__ == '__main__':
    app.run(debug=True)