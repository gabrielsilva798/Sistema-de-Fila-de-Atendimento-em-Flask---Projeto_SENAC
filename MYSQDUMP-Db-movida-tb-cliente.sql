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