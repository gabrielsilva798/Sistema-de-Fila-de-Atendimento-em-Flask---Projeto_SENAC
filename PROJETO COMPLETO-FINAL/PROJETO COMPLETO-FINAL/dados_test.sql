-- 1) Garantir que exista empresa com id = 5 (insere somente se não existir)
INSERT INTO tb_empresa (id, nome, cnpj, segmento, funcionarios, site, logo, email, telefone, cep, endereco, cidade, estado, senha, confirmar_senha, descricao)
SELECT 5, 'Clínica Brasília Saúde', '12.345.678/0001-99', 'Hospital', 50, 'https://brasiliasaude.example', NULL, 'contato@brasiliasaude.com', '(61)3333-4444', '70000-000', 'Av. Principal, 100', 'Brasília', 'DF', 'senha123', 'senha123', 'Unidade de teste para pacientes.'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM tb_empresa WHERE id = 5);

-- 2) Inserir pacientes um-a-um e guardar os ids em variáveis
-- Paciente 1
INSERT INTO pacientes (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
VALUES ('123.456.789-00', 'João Pereira', '1985-04-12', '(61)99999-1000', 'Dor de cabeça e febre', 'amarelo', 'Maria Pereira', 5);
SET @p1 = LAST_INSERT_ID();

-- Paciente 2
INSERT INTO pacientes (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
VALUES ('987.654.321-10', 'Ana Souza', '1992-09-30', '(61)98888-2001', 'Tosse e cansaço', 'verde', 'Carlos Souza', 5);
SET @p2 = LAST_INSERT_ID();

-- Paciente 3
INSERT INTO pacientes (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
VALUES ('456.789.123-55', 'Pedro Santos', '1978-01-22', '(61)97777-3002', 'Dor intensa no peito', 'vermelho', 'Juliana Santos', 5);
SET @p3 = LAST_INSERT_ID();

-- Paciente 4
INSERT INTO pacientes (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
VALUES ('321.654.987-99', 'Mariana Lima', '2003-07-11', '(61)98888-4003', 'Corte leve na mão', 'verde', 'Fabio Lima', 5);
SET @p4 = LAST_INSERT_ID();

-- Paciente 5
INSERT INTO pacientes (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
VALUES ('159.753.486-20', 'Carla Nascimento', '1999-12-05', '(61)96666-5004', 'Alergia forte', 'laranja', 'Rafael Nascimento', 5);
SET @p5 = LAST_INSERT_ID();

-- Paciente 6
INSERT INTO pacientes (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
VALUES ('789.456.123-33', 'Ricardo Oliveira', '1980-05-18', '(61)95555-6005', 'Pressão alta', 'amarelo', 'Bianca Oliveira', 5);
SET @p6 = LAST_INSERT_ID();

-- Paciente 7
INSERT INTO pacientes (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
VALUES ('951.357.258-44', 'Fernanda Ribeiro', '1975-03-14', '(61)94444-7006', 'Febre alta e tontura', 'laranja', 'José Ribeiro', 5);
SET @p7 = LAST_INSERT_ID();

-- Paciente 8
INSERT INTO pacientes (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
VALUES ('258.147.369-88', 'Lucas Almeida', '1996-06-27', '(61)93333-8007', 'Dificuldade para respirar', 'vermelho', 'Camila Almeida', 5);
SET @p8 = LAST_INSERT_ID();

-- Paciente 9
INSERT INTO pacientes (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
VALUES ('741.852.963-77', 'Bruno Cardoso', '2001-08-23', '(61)92222-9008', 'Dor abdominal persistente', 'amarelo', 'Patrícia Cardoso', 5);
SET @p9 = LAST_INSERT_ID();

-- Paciente 10
INSERT INTO pacientes (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
VALUES ('369.258.147-11', 'Gabriela Costa', '1994-02-09', '(61)91111-0009', 'Náuseas e vômitos', 'verde', 'Fernando Costa', 5);
SET @p10 = LAST_INSERT_ID();

-- 3) Inserir na fila usando os ids reais armazenados
INSERT INTO fila (paciente_id, empresa_id, chamado)
VALUES
(@p1, 5, FALSE),
(@p2, 5, FALSE),
(@p4, 5, TRUE),
(@p7, 5, FALSE),
(@p9, 5, TRUE);

-- 4) Inserir em_atendimento usando alguns pacientes (usando os mesmos dados do paciente)
INSERT INTO em_atendimento (paciente_id, empresa_id, cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel)
VALUES
(@p3, 5, '456.789.123-55', 'Pedro Santos', '1978-01-22', '(61)97777-3002', 'Dor intensa no peito', 'vermelho', 'Juliana Santos'),
(@p5, 5, '159.753.486-20', 'Carla Nascimento', '1999-12-05', '(61)96666-5004', 'Alergia forte', 'laranja', 'Rafael Nascimento'),
(@p8, 5, '258.147.369-88', 'Lucas Almeida', '1996-06-27', '(61)93333-8007', 'Dificuldade para respirar', 'vermelho', 'Camila Almeida');


 -- ---------------------------------------------------------------------------------------------------------------------------------------------------------
 INSERT INTO pacientes (cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel, empresa_id)
VALUES
('111.111.111-11', 'Marcos Almeida', '1988-05-12', '(61) 98888-1111', 'Febre, dor no corpo', 'amarelo', 'Esposa', 1),
('222.222.222-22', 'Fernanda Silva', '1995-09-23', '(61) 97777-2222', 'Dor abdominal intensa', 'vermelho', 'Mãe', 1),
('333.333.333-33', 'Carlos Santos', '1979-03-04', '(61) 96666-3333', 'Tosse forte e fadiga', 'laranja', 'Esposa', 1),
('444.444.444-44', 'Julia Ferreira', '2002-11-19', '(61) 95555-4444', 'Dor de cabeça, náusea', 'amarelo', 'Pai', 1),
('555.555.555-55', 'Roberta Nunes', '1983-07-30', '(61) 94444-5555', 'Corte superficial no braço', 'verde', 'Marido', 1);


INSERT INTO fila (paciente_id, empresa_id, chamado)
VALUES
(1, 1, FALSE),
(2, 1, TRUE),
(3, 1, FALSE),
(4, 1, FALSE),
(5, 1, TRUE);


INSERT INTO em_atendimento (paciente_id, empresa_id, cpf, nome, nascimento, telefone, sintomas, classificacao, responsavel)
VALUES
(2, 1, '222.222.222-22', 'Fernanda Silva', '1995-09-23', '(61) 97777-2222', 'Dor abdominal intensa', 'vermelho', 'Mãe'),
(5, 1, '555.555.555-55', 'Roberta Nunes', '1983-07-30', '(61) 94444-5555', 'Corte superficial no braço', 'verde', 'Marido'),
(3, 1, '333.333.333-33', 'Carlos Santos', '1979-03-04', '(61) 96666-3333', 'Tosse forte e fadiga', 'laranja', 'Esposa'),
(1, 1, '111.111.111-11', 'Marcos Almeida', '1988-05-12', '(61) 98888-1111', 'Febre, dor no corpo', 'amarelo', 'Esposa'),
(4, 1, '444.444.444-44', 'Julia Ferreira', '2002-11-19', '(61) 95555-4444', 'Dor de cabeça, náusea', 'amarelo', 'Pai');


INSERT INTO profissionais (
    id_empresa, nome_completo, data_nascimento, telefone, email_profissional,
    especialidade, registro_crm_coren, estado_crm, turno_atendimento,
    status_clinica, informacoes_adicionais
)
VALUES
(1, 'Dr. Ricardo Menezes', '1980-01-15', '(61) 99999-1001', 'ricardo.menezes@clinica.com', 'Clínico Geral', 'CRM12345', 'DF', 'Manhã', 'ativo', 'Experiente em emergência'),
(1, 'Dra. Helena Campos', '1987-04-22', '(61) 99999-1002', 'helena.campos@clinica.com', 'Pediatra', 'CRM54321', 'DF', 'Tarde', 'ativo', 'Atende crianças até 14 anos'),
(1, 'Enf. Paulo Oliveira', '1990-12-08', '(61) 99999-1003', 'paulo.oliveira@clinica.com', 'Enfermeiro', 'COREN99887', 'DF', 'Noite', 'ativo', 'Responsável por triagem'),
(1, 'Dra. Juliana Prado', '1985-06-19', '(61) 99999-1004', 'juliana.prado@clinica.com', 'Dermatologista', 'CRM77777', 'DF', 'Manhã', 'ferias', 'Retorna mês que vem'),
(1, 'Dr. Gustavo Farias', '1978-09-03', '(61) 99999-1005', 'gustavo.farias@clinica.com', 'Ortopedista', 'CRM11223', 'DF', 'Tarde', 'ativo', 'Especialista em fraturas');


