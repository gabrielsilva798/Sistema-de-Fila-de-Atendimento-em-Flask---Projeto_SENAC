# app/models.py
from app.db import get_db

# empresa
def create_empresa(data):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tb_empresa
        (nome, cnpj, segmento, funcionarios, site, email, telefone, cep, endereco, cidade, estado, senha, confirmar_senha, descricao)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data.get('nome'), data.get('cnpj'), data.get('segmento'), data.get('funcionarios'),
        data.get('site'), data.get('email'), data.get('telefone'), data.get('cep'),
        data.get('endereco'), data.get('cidade'), data.get('estado'),
        data.get('senha'), data.get('confirmar_senha'), data.get('descricao')
    ))
    conn.commit()
    cur.close()
    conn.close()
    return True

def get_empresa_by_email(email):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM tb_empresa WHERE email=%s", (email,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r

# cliente/paciente (usuário do sistema)
def create_cliente(data):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tb_clientes (nome, email, nascimento, cpf, rg, senha)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (data.get('nome'), data.get('email'), data.get('nascimento'), data.get('cpf'), data.get('rg'), data.get('senha')))
    conn.commit()
    cur.close()
    conn.close()
    return True

def get_cliente_by_email(email):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM tb_clientes WHERE email=%s", (email,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r

# fila/paciente/atendimento
def inserir_paciente_empresa(data, empresa_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    try:
        # Verifica se já existe paciente com mesmo CPF na mesma empresa
        cur.execute("""
            SELECT id 
            FROM pacientes 
            WHERE cpf = %s AND empresa_id = %s
        """, (data.get('cpf'), empresa_id))

        existente = cur.fetchone()

        if existente:
            paciente_id = existente['id']
        else:
            # Insere novo paciente com o ID do profissional responsável
            cur.execute("""
                INSERT INTO pacientes 
                (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                data.get('cpf'),
                data.get('nome'),
                data.get('nascimento'),
                data.get('telefone'),
                data.get('sintomas'),
                data.get('classificacao'),
                data.get('responsavel'),    # <-- ID do profissional
                empresa_id
            ))

            paciente_id = cur.lastrowid

        # Agora insere na fila
        cur.execute("""
            INSERT INTO fila (paciente_id, empresa_id)
            VALUES (%s, %s)
        """, (paciente_id, empresa_id))

        fila_id = cur.lastrowid

        conn.commit()

        return {"ok": True, "paciente_id": paciente_id, "fila_id": fila_id}

    finally:
        cur.close()
        conn.close()


def obter_fila_empresa(empresa_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT f.id AS fila_id, f.chegada, f.chamado, p.id AS paciente_id, p.nome, p.cpf, p.classificacao, p.entrada_inicio, p.entrada_fim
        FROM fila f JOIN pacientes p ON p.id=f.paciente_id
        WHERE f.empresa_id=%s ORDER BY f.chegada ASC
    """, (empresa_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def iniciar_atendimento(fila_id, empresa_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT f.paciente_id, p.cpf, p.nome, p.nascimento, p.telefone, 
               p.sintomas, p.classificacao, p.responsavel
        FROM fila f 
        JOIN pacientes p ON p.id = f.paciente_id
        WHERE f.id=%s AND f.empresa_id=%s
    """, (fila_id, empresa_id))

    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return {"ok": False}

    paciente_id = row['paciente_id']

    # Corrigido: agora tem *8 placeholders* igual às *8 colunas*
    cur.execute("""
        INSERT INTO em_atendimento 
        (paciente_id, empresa_id, cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        paciente_id,
        empresa_id,
        row['cpf'],
        row['nome'],
        row['nascimento'],
        row['telefone'],
        row['sintomas'],
        row['classificacao'],
        row['responsavel']  # SALVO AGORA
    ))

    em_id = cur.lastrowid

    cur.execute("DELETE FROM fila WHERE id=%s", (fila_id,))
    cur.execute("UPDATE pacientes SET entrada_fim=CURRENT_TIMESTAMP WHERE id=%s", (paciente_id,))
    conn.commit()

    cur.close()
    conn.close()

    return {"ok": True, "em_id": em_id}


def obter_em_atendimento(empresa_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM em_atendimento WHERE empresa_id=%s ORDER BY inicio_atendimento ASC", (empresa_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def remover_em_atendimento(em_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM em_atendimento WHERE id=%s", (em_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True


def limpar_fila_empresa(empresa_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM fila WHERE empresa_id=%s", (empresa_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True


def excluir_conta_empresa(empresa_id):
    conn = get_db()
    cur = conn.cursor()

    # Ordem correta: primeiro remover filas e atendimentos
    cur.execute("DELETE FROM fila WHERE empresa_id=%s", (empresa_id,))
    cur.execute("DELETE FROM em_atendimento WHERE empresa_id=%s", (empresa_id,))
    cur.execute("DELETE FROM pacientes WHERE empresa_id=%s", (empresa_id,))
    cur.execute("DELETE FROM profissionais WHERE id_empresa=%s", (empresa_id,))
    cur.execute("DELETE FROM tb_empresa WHERE id=%s", (empresa_id,))

    conn.commit()
    cur.close()
    conn.close()
    return True


def cadastrar_profissional_model(id_empresa, nome, data_nasc, telefone, email, especialidade,
                                 registro, estado_crm, turno, status, info_adicional):

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO profissionais (
                id_empresa, nome_completo, data_nascimento, telefone, email_profissional,
                especialidade, registro_crm_coren, estado_crm,
                turno_atendimento, status_clinica, informacoes_adicionais
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            id_empresa, nome, data_nasc, telefone, email, especialidade,
            registro, estado_crm, turno, status, info_adicional
        ))

        prof_id = cur.lastrowid
        conn.commit()
        return prof_id  # agora retorna o ID

    except Exception as e:
        print("Erro ao inserir profissional:", e)
        return None

    finally:
        cur.close()
        conn.close()
