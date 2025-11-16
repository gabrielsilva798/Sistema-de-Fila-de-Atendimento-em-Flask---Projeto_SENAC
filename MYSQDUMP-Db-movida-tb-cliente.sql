CREATE DATABASE db_movida CHARSET utf8mb4;

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    nascimento VARCHAR(20),
    cpf VARCHAR(20),
    rg VARCHAR(20),
    senha VARCHAR(100)
);

SELECT * FROM clientes;