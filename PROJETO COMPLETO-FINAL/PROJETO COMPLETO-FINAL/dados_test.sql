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
