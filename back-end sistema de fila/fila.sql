CREATE DATABASE IF NOT EXISTS db_movida;
USE db_movida;

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

CREATE TABLE IF NOT EXISTS fila (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    prioridade INT NOT NULL,
    chamado BOOLEAN DEFAULT FALSE,
    chegada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);
