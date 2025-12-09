-- 1. Garante que estamos usando o banco de dados correto
USE clinica_db;

-- 2. (Opcional) Se a tabela já existir e você quiser apagá-la para criar a nova:
-- DROP TABLE IF EXISTS profissionais;

-- 3. Cria a nova tabela 'profissionais' com os atributos solicitados
CREATE TABLE profissionais (
    -- ID e Chave Primária
    id INT NOT NULL AUTO_INCREMENT,
    
    -- Dados Pessoais
    nome_completo VARCHAR(150) NOT NULL,
    data_nascimento DATE, -- Usamos o tipo DATE para armazenar datas
    
    -- Dados de Contato
    telefone VARCHAR(15), -- Ex: (XX) 9XXXX-XXXX
    email_profissional VARCHAR(100) UNIQUE NOT NULL, -- UNIQUE garante que não haja 2 profissionais com o mesmo email
    
    -- Dados de Registro Profissional
    especialidade VARCHAR(50) NOT NULL, -- Armazenará uma das opções do SELECT
    registro_crm_coren VARCHAR(20) UNIQUE NOT NULL, -- Ex: CRM: 12345 ou COREN: 98765
    estado_crm VARCHAR(2) NOT NULL, -- Armazenará a sigla do estado (Ex: SP, RJ, MG)
    
    -- Dados de Atendimento
    turno_atendimento VARCHAR(10) NOT NULL, -- Armazenará 'Manhã', 'Tarde', 'Noite' ou 'Integral
    status_clinica VARCHAR(15) NOT NULL,
    
    -- Informações Adicionais
    informacoes_adicionais TEXT, -- Usamos TEXT para campos longos
    
    PRIMARY KEY (id)
);