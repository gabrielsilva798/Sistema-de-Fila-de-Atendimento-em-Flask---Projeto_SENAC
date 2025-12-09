-- 1. Garante que estamos usando o banco de dados correto
USE clinica_db;

-- 2. (Opcional) Se a tabela já existir e você quiser apagá-la para criar a nova:
-- DROP TABLE IF EXISTS profissionais;

-- 3. Cria a nova tabela 'profissionais' com os atributos solicitados
CREATE TABLE profissionais (
    id INT NOT NULL AUTO_INCREMENT,
    nome_completo VARCHAR(150) NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(15),
    email_profissional VARCHAR(100) UNIQUE NOT NULL,
    especialidade VARCHAR(50) NOT NULL, 
    registro_crm_coren VARCHAR(20) UNIQUE NOT NULL,
    estado_crm VARCHAR(2) NOT NULL, 
    turno_atendimento VARCHAR(10) NOT NULL,
    status_clinica VARCHAR(15) NOT NULL,
    informacoes_adicionais TEXT,
    PRIMARY KEY (id)
);