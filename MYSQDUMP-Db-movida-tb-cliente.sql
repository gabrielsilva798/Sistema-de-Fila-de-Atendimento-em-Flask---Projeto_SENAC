CREATE DATABASE IF NOT EXISTS db_movida
CHARSET utf8mb4
COLLATE utf8mb4_general_ci;

USE db_movida;

CREATE TABLE tb_clientes (
    id INT  PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    nascimento VARCHAR(20),
    cpf VARCHAR(20) UNIQUE,
    rg VARCHAR(20) UNIQUE,
    senha VARCHAR(100),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM tb_clientes;
DELETE FROM tb_clientes WHERE id = 1;

/*-------------------------------------------------------------------------------------------------*/

CREATE TABLE tb_empresa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    segmento ENUM('Clinica particular', 'Clinica pública', 'Hospital') NOT NULL,
    funcionarios INT DEFAULT NULL,
    site VARCHAR(255) DEFAULT NULL,
    logo LONGBLOB DEFAULT NULL,
    email VARCHAR(150) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    cep VARCHAR(9) NOT NULL,
    endereco VARCHAR(200) NOT NULL,
    cidade VARCHAR(120) NOT NULL,
    estado CHAR(2) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    confirmar_senha VARCHAR(255) NOT NULL,
    descricao TEXT
);


SELECT * FROM tb_empresa;
DELETE FROM tb_empresa WHERE id = 1;
#--------------------------------------------------- FILA ---------------------------------------

-- TABELA: pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cpf VARCHAR(20),
    nome VARCHAR(255),
    nascimento DATE,
    telefone VARCHAR(20),
    sintomas TEXT,
    classificacao ENUM('verde','amarelo','laranja','vermelho'),
    responsavel VARCHAR(255)
);

-- TABELA: fila
CREATE TABLE IF NOT EXISTS fila (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    chamado BOOLEAN DEFAULT FALSE,
    chegada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);
