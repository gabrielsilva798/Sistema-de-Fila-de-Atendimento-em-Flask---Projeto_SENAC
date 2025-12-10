CREATE DATABASE IF NOT EXISTS db_movida
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;
USE db_movida;

-- SELECT * FROM tb_clientes;
CREATE TABLE IF NOT EXISTS tb_clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    nascimento VARCHAR(20),
    cpf VARCHAR(20) UNIQUE,
    rg VARCHAR(20) UNIQUE,
    senha VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SELECT * FROM tb_empresa;
-- UPDATE tb_empresa SET id=5 WHERE id=1;
CREATE TABLE IF NOT EXISTS tb_empresa (
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
    descricao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SELECT * FROM pacientes;
CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cpf VARCHAR(20),
    nome VARCHAR(255),
    nascimento DATE,
    telefone VARCHAR(20),
    sintomas TEXT,
    classificacao ENUM('verde','amarelo','laranja','vermelho'),
    responsavel INT NOT NULL,
    empresa_id INT,
    entrada_inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    entrada_fim TIMESTAMP NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empresa_id) REFERENCES tb_empresa(id) ON DELETE CASCADE,
    FOREIGN KEY (responsável) REFERENCES profissionais(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SELECT * FROM fila;
CREATE TABLE IF NOT EXISTS fila (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    empresa_id INT NOT NULL,
    chamado BOOLEAN DEFAULT FALSE,
    chegada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (empresa_id) REFERENCES tb_empresa(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SELECT * FROM em_atendimento;
CREATE TABLE IF NOT EXISTS em_atendimento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    empresa_id INT,
    cpf VARCHAR(20),
    nome VARCHAR(255),
    nascimento DATE,
    telefone VARCHAR(20),
    sintomas TEXT,
    classificacao ENUM('verde','amarelo','laranja','vermelho'),
    responsavel VARCHAR(255),
    inicio_atendimento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fim_atendimento TIMESTAMP NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE SET NULL,
    FOREIGN KEY (empresa_id) REFERENCES tb_empresa(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_pacientes_empresa_cpf ON pacientes(empresa_id, cpf);
CREATE INDEX idx_fila_empresa_chegada ON fila(empresa_id, chegada);

-- SELECT * FROM profissionais;
CREATE TABLE profissionais (
    id INT NOT NULL AUTO_INCREMENT,
    id_empresa INT NOT NULL,
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
    FOREIGN KEY (id_empresa) REFERENCES tb_empresa(id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);