# 🏥 Sistema de Fila Hospitalar em Tempo Real
### 🥂INTEGRANTES
* Gabriel Silva dos Santos
* Gilcelio da Silva Santos Júnior
* Valérya Dias Braga
* Tais Carvalho Nascimento
---
## 📌 Visão Geral

Este projeto consiste em um **Sistema de Fila de Espera para Hospitais e Clínicas**, desenvolvido em **Python com Flask**, cujo principal diferencial é permitir que o **paciente acompanhe sua posição na fila em tempo real diretamente pelo celular ou navegador**.

O sistema foi pensado para melhorar a experiência do paciente e otimizar a gestão do estabelecimento de saúde, trazendo **transparência**, **previsibilidade** e **organização** ao processo de atendimento.

![Langinpage](img/landingpage.png)

---

## 🚀 Diferencial do Projeto

O grande diferencial do sistema é o **acompanhamento online da fila em tempo real**, permitindo que o paciente:

* Saiba exatamente **qual é sua posição na fila**;
* Veja o **tempo estimado de espera**;
* Consulte sua **classificação de risco**;
* Acompanhe os **últimos pacientes chamados** e os **próximos da fila**.

Isso possibilita que o paciente possa, por exemplo:

* Ir comprar algo;
* Buscar um filho na escola;
* Se deslocar com mais tranquilidade;

Tudo isso sem o medo de perder sua vez, pois ele tem **previsibilidade do atendimento**.

![página de login](img/login.png)
---

## 👤 Funcionalidades do Paciente

Cada paciente possui um **ambiente próprio**, acessado por login.

No painel do paciente, é possível visualizar:

* 📍 **Posição atual na fila** (em tempo real);
* ⏱️ **Tempo estimado de espera**;
* 🚦 **Classificação de risco**:

  * Verde
  * Amarelo
  * Laranja
  * Vermelho
* 👨‍⚕️ **Os 5 últimos pacientes chamados (em atendimento)**;
* 👥 **Os 5 primeiros pacientes ainda aguardando na fila**.

Essas informações são atualizadas dinamicamente, garantindo **transparência e confiança**.

![Fila do paciente](img/fila_paciente.png)

---

## 🏥 Funcionalidades do Estabelecimento (Hospital / Clínica)

O estabelecimento possui um **ambiente administrativo exclusivo**, acessado por login próprio.

### 📋 Gerenciamento da Fila

O estabelecimento pode:

* Adicionar pacientes à fila;
* Visualizar a fila **em tempo real**;
* Ver quais pacientes estão **aguardando** e quais estão **em atendimento**;
* Iniciar atendimento de um paciente;
* Finalizar atendimento;
* Remover pacientes da fila ao encerrar o atendimento.

Página de cadastro dos pacientes na fila
![página de cadstrar pacientes](img/adc_pacientes.png)

Fila de espera

![página lista de pacientes](img/lista_paciente.png)

### 📊 Indicadores em Tempo Real

O sistema exibe automaticamente:

* Quantidade de pacientes:

  * 🧍 Na fila de espera;
  * 🩺 Em atendimento;
  * ✅ Atendimentos encerrados no dia.

![dashboard](img/dashboard.png)
---

## 👨‍⚕️ Cadastro de Profissionais de Saúde

A clínica pode:

* Cadastrar médicos e profissionais no sistema;
* Selecionar o profissional responsável **no momento de iniciar um atendimento**;

Isso garante melhor organização e rastreabilidade dos atendimentos realizados.

Gerenciamento de Profissionais
![Profissionais](img/profissionais.png)

Cdastro de Profissionais
![Cadastrar novo Profissionais](img/cad_profissionais.png)

---

## 📈 Análise de Dados (Business Intelligence)

O sistema conta com uma **área de análise de dados**, onde o estabelecimento pode:

* Fazer perguntas sobre os dados do próprio estabelecimento;
* Receber como resposta:

  * 📊 **Gráficos gerados com Matplotlib**;<br>
  ![Gráfico](img/grafico.png)
  * 📋 **Tabelas geradas com Pandas**;<br>
  ![tabela](img/pandas.png)

Esses recursos auxiliam na tomada de decisão, análise de fluxo de pacientes e desempenho diário.

---

## ⚙️ Configurações do Estabelecimento

Na área de configurações, o estabelecimento pode:

* Alterar o nome da empresa;
* Atualizar o e-mail de acesso;
* Ativar ou desativar notificações;
* Excluir a conta do sistema.<br>
![configuracoes](img/configuracoes.png)

---

## 🛠️ Tecnologias Utilizadas

O projeto foi desenvolvido em **Python**, utilizando as seguintes tecnologias e bibliotecas:

### Backend

* **Flask** (framework web)
* **Werkzeug** (segurança de senhas)
* **MySQL Connector** (conexão com banco de dados MySQL)
* **dotenv** (variáveis de ambiente)

### Manipulação de Dados e Gráficos

* **Pandas** (análise e manipulação de dados)
* **Matplotlib** (geração de gráficos)

## ☁ Deploy na AWS
Nosso sistema está pronto e documentado para computação em nuvem usando serviços da Cloud da AWS como:
* <b>AWS EC2</b> (opcional ao ECS e FARGATE)
* <b>AWS ECS</b>  (opcional ao FARGATE e EC2)
* <b>AWS FARGATE</b> (opcional ao ECS e EC2)
* <b>AWS RDS</b> (mysql)
* <b>AWS VPC</b> (configurações de rede)
* <b>AWS ALB</b> (para uma arquitetura sem gargalos)
* <b>AWS AUTO SCALING</b> (para uma arquitetura escalável)
* <b>AWS IAM</b> (para comunicação entre os serviços via Roles)
* <b>AWS SECURITY GROUPS</b> (firewall para permitir somente as comunicações necessárias)
* <b>AWS CLOUDWACTH</b> (para analisar o desempenho e gargalos em nossos serviços)

Teremos 3 cenários para implantar o serviço via container (Docker):
* 1º com EC2 (posso implantar em container ou não)
* 2º com ECS (serviço gerenciado de containers)
* 3º com FARGATE (serviço gerenciado e serveless)

---
### 🐳 Docker

A aplicação é executada em um **container Docker**, garantindo padronização entre ambientes de desenvolvimento e produção.  
O backend Flask roda com **Gunicorn + Eventlet**, assegurando suporte a **Socket.IO** e comunicação em tempo real.

- Porta interna do container: **8000**
- Variáveis sensíveis via **.env**
- Compatível com **AWS EC2, ECS e ECS Fargate**
- Pronto para integração com **ALB e Auto Scaling**
---
## 🛠️ Tecnologias, Bibliotecas e Dependências
#### 🌐 Framework Web

* Flask

* render_template

* request

* redirect

* url_for

* session

* flash

* jsonify

* Response

#### 🔐 Segurança e Autenticação

* Werkzeug Security

* generate_password_hash

* check_password_hash

#### 🕒 Manipulação de Datas e Horários

* Datetime

* datetime

#### 🗄️ Banco de Dados

* MySQL Connector

* mysql.connector.Error

* Camada de acesso ao banco

* get_db

* Models da aplicação

* app.models

#### 📊 Análise de Dados e Visualização

* Pandas

* Matplotlib

#### 🤖 Inteligência Artificial e Processamento de Dados

* Gemini AI

* gemini_instrucao_segura

* Operações com Pandas

* executar_operacao

#### ⚙️ Utilitários e Configurações

* dotenv

* load_dotenv

* Funções utilitárias

* functools.wraps

* Manipulação de arquivos e sistema

* os

* io

* json

---

## 🗂️ Estrutura Geral do Sistema

* **Autenticação separada** para paciente e estabelecimento;
* **Sessões seguras** para controle de acesso;
* **Atualização em tempo real da fila**;
* **Integração entre dados operacionais e análise de dados**;
* **Arquitetura modular**, facilitando manutenção e evolução do projeto.

---

## 🎯 Objetivo do Projeto

O objetivo principal é:

* Melhorar a experiência do paciente;
* Reduzir filas físicas e aglomerações;
* Oferecer dados estratégicos para o estabelecimento;
* Tornar o atendimento mais humano, previsível e eficiente.

---

📄 **Projeto desenvolvido com foco em usabilidade, organização e análise de dados.**
---
## 📌 Documentação das Rotas

---

## 🌐 Rotas Públicas

### `/`
- **Método:** `GET`
- **Descrição:**  
  Página inicial do sistema (landing page), acessível tanto para **pacientes** quanto para **estabelecimentos**.

---

## 🏥 Rotas do Estabelecimento (Hospital / Clínica)

### `/registrar_empresa`
- **Métodos:** `GET`, `POST`
- **Descrição:**
  - **GET:** Exibe o formulário de cadastro do estabelecimento
  - **POST:** Registra uma nova empresa no sistema, com validação de senha e dados institucionais

---

### `/login_estabelecimento`
- **Método:** `GET`
- **Descrição:**  
  Exibe a página de login do estabelecimento.

---

### `/login_empresa`
- **Método:** `POST`
- **Descrição:**  
  Processa o login do estabelecimento, valida credenciais e cria uma sessão segura.

---

### `/logout` | `/logout_estabelecimento`
- **Método:** `GET`
- **Descrição:**  
  Realiza o logout do estabelecimento, limpa a sessão e atualiza a fila em tempo real via **Socket.IO**.

---

### `/tela-principal-estabelecimento`
- **Método:** `GET`
- **Descrição:**  
  Painel principal do estabelecimento, exibindo os **pacientes atualmente em atendimento**.

---

## 👤 Rotas do Paciente (Cliente)

### `/login_cadastro_paciente`
- **Método:** `GET`
- **Descrição:**  
  Exibe a tela unificada de **login e cadastro** do paciente.

---

### `/registrar_cliente`
- **Método:** `POST`
- **Descrição:**  
  Cria uma nova conta de paciente com validações de segurança:
  - Senha mínima
  - Confirmação de senha

---

### `/login_cliente`
- **Método:** `POST`
- **Descrição:**  
  Autentica o paciente e inicia sua sessão no sistema.

---

### `/logout_cliente`
- **Método:** `GET`
- **Descrição:**  
  Encerra a sessão do paciente, mantendo intacta a sessão do estabelecimento.

---

### `/fila`
- **Método:** `GET`
- **Descrição:**  
  Painel do paciente para acompanhamento da fila em tempo real, exibindo:
  - 🔢 Posição atual na fila
  - ⏳ Tempo médio estimado de espera
  - 🚦 Classificação de risco
  - 👥 Últimos pacientes atendidos

---

## 📡 APIs (Dados em Tempo Real)

### `/api/primeiros_fila`
- **Método:** `GET`
- **Descrição:**  
  Retorna os **4 primeiros pacientes na fila de espera**, incluindo:
  - Nome
  - Classificação
  - Posição

---

### `/api/em_atendimento`
- **Método:** `GET`
- **Descrição:**  
  Retorna os **4 pacientes atualmente em atendimento**, com horário de início.

---

## 🔄 WebSocket — Atualização em Tempo Real

### Namespace: `/fila`

#### Evento: `connect`
- **Descrição:**  
  Disparado quando um paciente se conecta ao sistema de fila.

---

#### Evento: `join_fila`
- **Descrição:**  
  O paciente entra na fila e inicia uma **thread dedicada**, que atualiza sua posição a cada **3 segundos**.

---

#### Evento emitido: `fila_update`
- **Descrição:**  
  Envia automaticamente ao paciente:
  - Posição atual
  - Tempo médio estimado
  - Classificação de risco
  - Últimos atendimentos

---

## 🧍‍♂️ Gerenciamento de Pacientes (Estabelecimento)

### `/cadastrar-paciente`
- **Método:** `GET`
- **Descrição:**  
  Exibe o formulário para cadastro de pacientes na fila, incluindo seleção do **profissional responsável**.

---

### `/cadastro`
- **Método:** `POST`
- **Descrição:**  
  Insere o paciente na fila do estabelecimento e notifica todos os clientes conectados em tempo real.

---

### `/lista-pacientes`
- **Método:** `GET`
- **Descrição:**  
  Lista todos os pacientes aguardando atendimento na fila.

---

### `/iniciar_atendimento/<fila_id>`
- **Método:** `POST`
- **Descrição:**  
  Move o paciente da fila para o estado **em atendimento**, atualizando todos os painéis em tempo real.

---

### `/remover_em_atendimento/<em_id>`
- **Método:** `POST`
- **Descrição:**  
  Finaliza o atendimento do paciente e remove do estado ativo.

---

## ⚙️ Configurações do Estabelecimento

### `/configuracoes-estabelecimento` | `/config_empresa`
- **Métodos:** `GET`, `POST`
- **Descrição:**  
  Permite:
  - ✏️ Alterar nome da empresa
  - ⚙️ Gerenciar configurações gerais

---

### `/excluir_conta`
- **Método:** `POST`
- **Descrição:**  
  Exclui permanentemente a conta do estabelecimento e todos os dados relacionados.

---

## 🤖 Módulo de Análise de Dados (Gemini + Pandas)

### `/gemini`
- **Método:** `GET`
- **Descrição:**  
  Exibe a interface de **análise inteligente de dados** do estabelecimento.

---

### `/gemini/tabela`
- **Método:** `POST`
- **Descrição:**  
  Gera uma **tabela dinâmica com Pandas**, baseada em um prompt do usuário e dados reais do sistema.

---

### `/gemini/grafico`
- **Método:** `POST`
- **Descrição:**  
  Retorna um **gráfico gerado com Matplotlib**, conforme solicitação do usuário.

---

## 👨‍⚕️ Gestão de Profissionais de Saúde

### `/profissionais`
- **Métodos:** `GET`, `POST`
- **Descrição:**  
  Lista profissionais cadastrados, com filtros por:
  - Especialidade
  - Status

---

### `/cadastrar-profissional`
- **Métodos:** `GET`, `POST`
- **Descrição:**  
  Cadastra novos médicos ou profissionais de saúde no sistema.

---

### `/editar-profissional/<id>`
- **Métodos:** `GET`, `POST`
- **Descrição:**  
  Edita os dados de um profissional já cadastrado.

---

### `/excluir-profissional`
- **Método:** `POST`
- **Descrição:**  
  Remove um profissional do sistema.
---

## 🔄 Diagrama de Fluxo das Rotas do Sistema

### 👤 Diagrama — Fluxo do Paciente
flowchart TD
    A[👤 Paciente] --> B[/login_cadastro_paciente/]

    B -->|Cadastro| C[/registrar_cliente/]
    B -->|Login| D[/login_cliente/]

    D --> E[📊 Painel do Paciente]
    E --> F[/fila/]

    F -->|Conexão| WS[[🔄 WebSocket /fila]]
    WS -->|fila_update| F

    E --> G[/logout_cliente/]
🔎 O que este diagrama representa

* Autenticação do paciente

* Acesso ao painel de acompanhamento da fila

* Atualizações em tempo real

* Encerramento da sessão
---
### 🏥 Diagrama — Fluxo do Estabelecimento
flowchart TD
    A[🏥 Estabelecimento] --> B[/login_estabelecimento/]

    B -->|Cadastro| C[/registrar_empresa/]
    B -->|Login| D[/login_empresa/]

    D --> E[🏥 Painel do Estabelecimento]
    E --> F[/tela-principal-estabelecimento/]

    %% Gestão de Pacientes
    F --> G[/cadastrar-paciente/]
    G --> H[/cadastro/]
    F --> I[/lista-pacientes/]

    I -->|Iniciar Atendimento| J[/iniciar_atendimento/]
    F -->|Finalizar Atendimento| K[/remover_em_atendimento/]

    %% Profissionais
    F --> L[/profissionais/]
    L --> M[/cadastrar-profissional/]
    L --> N[/editar-profissional/]
    L --> O[/excluir-profissional/]

    %% Configurações
    F --> P[/config_empresa/]
    P --> Q[/excluir_conta/]

    %% Análise de Dados
    F --> R[/gemini/]
    R --> S[/gemini/tabela/]
    R --> T[/gemini/grafico/]

    %% Logout
    F --> U[/logout_estabelecimento/]
🔎 O que este diagrama representa

* Autenticação do estabelecimento

* Gestão completa da fila

* Profissionais de saúde

* Configurações da empresa

* Análise de dados com IA
---
### 📡 Diagrama — API & WebSocket (Tempo Real)
flowchart TD
    A[🖥️ Frontend] --> B[🌐 API Flask]

    %% APIs REST
    B --> C[/api/primeiros_fila/]
    B --> D[/api/em_atendimento/]

    %% WebSocket
    B --> WS[[🔄 WebSocket /fila]]

    WS -->|connect| E[👤 Paciente]
    WS -->|join_fila| F[📊 Monitoramento]

    F -->|fila_update (3s)| WS
    WS -->|Atualização| E

    %% Backend
    B --> DB[(🗄️ MySQL)]
🔎 O que este diagrama representa

* Comunicação REST para leitura de dados

* Comunicação WebSocket para tempo real

* Atualizações automáticas da fila

* Integração com banco de 
---
# 📊 Documentação do Banco de Dados – db_movida

Este documento descreve a estrutura do banco de dados **db_movida**, utilizado em um sistema de gerenciamento clínico com controle de empresas, pacientes, fila de atendimento, atendimentos em andamento e profissionais de saúde.

---

## 🗄️ Informações Gerais

- **Banco de Dados:** `db_movida`
- **SGBD:** MySQL / MariaDB
- **Charset:** `utf8mb4`
- **Collation:** `utf8mb4_general_ci`
- **Engine:** InnoDB

---
## 🍅 Modelo lógico
![modelo_logico](img/modelo_logico.png)
---

## 🧩 Estrutura das Tabelas

### 👤 tb_clientes
Armazena os dados de clientes do sistema.

| Campo        | Tipo            | Descrição |
|--------------|-----------------|-----------|
| id           | INT (PK)        | Identificador único |
| nome         | VARCHAR(100)    | Nome do cliente |
| email        | VARCHAR(100)    | Email único |
| nascimento   | VARCHAR(20)     | Data de nascimento |
| cpf          | VARCHAR(20)     | CPF único |
| rg           | VARCHAR(20)     | RG único |
| senha        | VARCHAR(255)    | Senha criptografada |
| criado_em    | TIMESTAMP       | Data de criação |

---

### 🏢 tb_empresa
Representa clínicas, hospitais ou empresas de saúde.

| Campo             | Tipo | Descrição |
|-------------------|------|-----------|
| id                | INT (PK) | Identificador da empresa |
| nome              | VARCHAR(150) | Nome da empresa |
| cnpj              | VARCHAR(18) | CNPJ único |
| segmento          | ENUM | Tipo de instituição |
| funcionarios      | INT | Quantidade de funcionários |
| site              | VARCHAR(255) | Site institucional |
| logo              | LONGBLOB | Logo da empresa |
| email             | VARCHAR(150) | Email |
| telefone          | VARCHAR(20) | Telefone |
| cep               | VARCHAR(9) | CEP |
| endereco          | VARCHAR(200) | Endereço |
| cidade            | VARCHAR(120) | Cidade |
| estado             | CHAR(2) | UF |
| senha             | VARCHAR(255) | Senha |
| confirmar_senha   | VARCHAR(255) | Confirmação da senha |
| descricao         | TEXT | Descrição |
| criado_em         | TIMESTAMP | Data de criação |

---

### 🧑‍⚕️ pacientes
Armazena pacientes vinculados a uma empresa.

| Campo | Tipo | Descrição |
|------|------|-----------|
| id | INT (PK) | Identificador do paciente |
| cpf | VARCHAR(20) | CPF |
| nome | VARCHAR(255) | Nome |
| nascimento | DATE | Data de nascimento |
| telefone | VARCHAR(20) | Telefone |
| sintomas | TEXT | Sintomas relatados |
| classificacao | ENUM | Nível de urgência |
| responsavel | VARCHAR(255) | Responsável |
| empresa_id | INT (FK) | Empresa vinculada |
| entrada_inicio | TIMESTAMP | Entrada do paciente |
| entrada_fim | TIMESTAMP | Saída |
| criado_em | TIMESTAMP | Registro |

🔗 **Relacionamento:**  
`pacientes.empresa_id → tb_empresa.id`

---

### ⏳ fila
Controla a fila de atendimento.

| Campo | Tipo | Descrição |
|------|------|-----------|
| id | INT (PK) | Identificador |
| paciente_id | INT (FK) | Paciente |
| empresa_id | INT (FK) | Empresa |
| chamado | BOOLEAN | Se foi chamado |
| chegada | TIMESTAMP | Horário de chegada |
| criado_em | TIMESTAMP | Registro |

🔗 **Relacionamentos:**  
- `paciente_id → pacientes.id`  
- `empresa_id → tb_empresa.id`

---

### 🩺 em_atendimento
Pacientes atualmente em atendimento.

| Campo | Tipo | Descrição |
|------|------|-----------|
| id | INT (PK) | Identificador |
| paciente_id | INT (FK) | Paciente |
| empresa_id | INT (FK) | Empresa |
| cpf | VARCHAR(20) | CPF |
| nome | VARCHAR(255) | Nome |
| nascimento | DATE | Nascimento |
| telefone | VARCHAR(20) | Telefone |
| sintomas | TEXT | Sintomas |
| classificacao | ENUM | Urgência |
| responsavel | VARCHAR(255) | Responsável |
| inicio_atendimento | TIMESTAMP | Início |
| fim_atendimento | TIMESTAMP | Fim |
| criado_em | TIMESTAMP | Registro |

---

### 👨‍⚕️ profissionais
Cadastro de profissionais da saúde.

| Campo | Tipo | Descrição |
|------|------|-----------|
| id | INT (PK) | Identificador |
| id_empresa | INT (FK) | Empresa |
| nome_completo | VARCHAR(150) | Nome |
| data_nascimento | DATE | Nascimento |
| telefone | VARCHAR(15) | Telefone |
| email_profissional | VARCHAR(100) | Email |
| especialidade | VARCHAR(50) | Especialidade |
| registro_crm_coren | VARCHAR(20) | Registro |
| estado_crm | CHAR(2) | UF |
| turno_atendimento | VARCHAR(10) | Turno |
| status_clinica | VARCHAR(15) | Status |
| informacoes_adicionais | TEXT | Observações |

---

## ⚡ Índices Criados

- `idx_pacientes_empresa_cpf` → otimiza buscas por empresa e CPF
- `idx_fila_empresa_chegada` → melhora ordenação da fila

---

## 🔗 Relacionamentos Principais

- Uma **empresa** pode ter vários **pacientes**
- Um **paciente** pode estar na **fila** ou em **atendimento**
- Uma **empresa** possui vários **profissionais**

---

## 💾 Observações Finais sobre o DATABASE

Este banco foi projetado para:
- Suportar múltiplas empresas
- Controlar filas de atendimento
- Registrar atendimentos em tempo real
- Garantir integridade referencial com `FOREIGN KEYS`

---

### 📂 **Arquivo de inicialização:** `db_init.sql`
---
## 🐳 Docker – Containerização da Aplicação

Este projeto utiliza **Docker** para padronizar o ambiente de execução da aplicação, facilitando o desenvolvimento local e o deploy em ambientes cloud como **AWS EC2, ECS e ECS Fargate**.

A aplicação Flask é executada em produção utilizando **Gunicorn** com **Eventlet**, garantindo suporte a **Socket.IO** e comunicação em tempo real.

---

### 📄 Dockerfile

```dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    default-libmysqlclient-dev \
    python3-dev \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:8000", "main:app"]
```

---

### ▶️ Build da Imagem Docker

```bash
docker build -t projeto-movida .
```

---

### 🚀 Execução do Container

```bash
docker run -d \
  --name projeto-movida \
  --env-file .env \
  -p 5000:8000 \
  projeto-movida
```

A aplicação ficará disponível em:

```
http://localhost:5000
```

---

### 🔑 Observações Importantes

- A aplicação roda **internamente na porta 8000**
- A porta externa pode ser mapeada livremente (ex: `5000:8000`)
- O arquivo `.env` **não é versionado** e é injetado em tempo de execução
- Compatível com **Application Load Balancer (ALB)** da AWS
- Suporte completo a **WebSocket / Socket.IO**
- Pronto para **ECS e ECS Fargate**

---

### ✅ Benefícios do Uso do Docker

- Ambiente consistente entre desenvolvimento e produção
- Deploy simplificado
- Facilidade de escalabilidade
- Integração com pipelines de CI/CD

📌 *Esta configuração segue boas práticas de containerização e arquitetura cloud moderna.*

---
# 🏥 Documentação Completa de Deploy na AWS

## Sistema de Fila Hospitalar em Tempo Real

Esta documentação descreve **uma arquitetura completa, segura e profissional na AWS** para o Sistema de Fila Hospitalar em Tempo Real, utilizando:

* **Docker** para containerização da aplicação Flask
* **Amazon RDS (MySQL)** como banco de dados gerenciado
* **VPC personalizada com subnets públicas e privadas**
* **IAM Roles e Policies** para comunicação segura entre serviços
* **Cenários de deploy com EC2, ECS ou ECS Fargate**

O objetivo é permitir que este material seja **copiado diretamente para o GitHub**, servindo como **documentação técnica, portfólio e base de estudo para Cloud / DevOps**.

---

## 📌 Visão Geral da Arquitetura

A aplicação roda em containers Docker e se comunica com o banco MySQL hospedado no Amazon RDS, dentro de uma VPC isolada.

### 📐 Arquitetura Geral

```
Internet
   ↓
Application Load Balancer (opcional)
   ↓
EC2 ou ECS/Fargate (Container Flask)
   ↓
Amazon RDS MySQL (Subnet Privada)
```

---

## ☁️ Serviços AWS Utilizados

* Amazon VPC
* Amazon EC2
* Amazon ECS / ECS Fargate
* Amazon RDS (MySQL)
* Amazon ECR
* IAM (Roles e Policies)
* Application Load Balancer (ALB)
* CloudWatch Logs
* Security Groups

---

## 🌐 VPC – Configuração de Rede

### 🧱 Estrutura da VPC

* CIDR da VPC: `10.0.0.0/16`

### 🔹 Subnets

| Tipo             | CIDR        | AZ         | Uso       |
| ---------------- | ----------- | ---------- | --------- |
| Subnet Pública A | 10.0.1.0/24 | us-east-1a | ALB / EC2 |
| Subnet Pública B | 10.0.2.0/24 | us-east-1b | ALB       |
| Subnet Privada A | 10.0.3.0/24 | us-east-1a | ECS / RDS |
| Subnet Privada B | 10.0.4.0/24 | us-east-1b | ECS / RDS |

### 🌍 Internet Gateway

* Associado à VPC
* Usado apenas pelas subnets públicas

### 🔁 NAT Gateway

* Criado em subnet pública
* Permite acesso à internet para recursos em subnets privadas (ex: ECS baixar imagens)

---

## 🔐 Security Groups (Segurança de Rede)

### 🔸 SG – Application Load Balancer

* Entrada:

  * HTTP 80 (0.0.0.0/0)
  * HTTPS 443 (0.0.0.0/0)
* Saída:

  * All traffic

### 🔸 SG – EC2 / ECS Tasks

* Entrada:

  * Porta 8000 (somente do SG do ALB)
* Saída:

  * All traffic

### 🔸 SG – RDS MySQL

* Entrada:

  * Porta 3306 (somente do SG da aplicação)
* Saída:

  * All traffic

---

## 🗄️ Amazon RDS – Configuração Completa

### 🔧 Parâmetros do Banco

* Engine: MySQL
* Versão: 8.x
* Tipo: db.t3.micro (Free Tier)
* Multi-AZ: Opcional
* Storage: GP2 / GP3
* Backup automático: Ativado
* Retenção: 7 dias

### 🔐 Segurança

* RDS em **subnets privadas**
* Acesso público: ❌ Desativado
* Credenciais fora do código

---

## 🐳 Containerização da Aplicação

### 📁 Estrutura do Projeto

```
Sistema-Fila-Hospitalar/
│── app/
│── static/
│── templates/
│── app.py
│── requirements.txt
│── Dockerfile
│── .dockerignore
│── .env (não versionado)
```

### 🧱 Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
```

---

## 🔐 IAM – Roles e Permissões

### 🔹 Role para EC2 (EC2InstanceRole)

Permite:

* Pull de imagens no ECR
* Escrita de logs no CloudWatch

Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

---

### 🔹 Role para ECS Task (ecsTaskExecutionRole)

Permite:

* Pull de imagens no ECR
* Logs no CloudWatch

Policies gerenciadas:

* AmazonECSTaskExecutionRolePolicy

---

## 🚀 Cenários de Deploy

---

## 🔵 CENÁRIO 1 — EC2 + Docker

### 📌 Fluxo

```
Internet → EC2 → Container Flask → RDS
```

### ✅ Vantagens

* Simples
* Ideal para portfólio

### ❌ Desvantagens

* Escalabilidade manual

---

## 🟣 CENÁRIO 2 — ECS (EC2 Launch Type)

### 📌 Fluxo

```
Internet → ALB → ECS Cluster → Tasks → RDS
```

### ✅ Vantagens

* Alta disponibilidade
* Controle de instâncias

---

## 🟢 CENÁRIO 3 — ECS Fargate (Recomendado)

### 📌 Fluxo

```
Internet → ALB → ECS Fargate → RDS
```

### ✅ Vantagens

* Sem servidores
* Escalabilidade automática
* Arquitetura moderna

---

## 🌐 Application Load Balancer

* Listener HTTP 80 / HTTPS 443
* Target Group: porta 8000
* Health Check: `/`

---

## 🔐 Variáveis de Ambiente

```env
FLASK_ENV=production
SECRET_KEY=sua_secret_key
DB_HOST=endpoint-rds
DB_USER=admin
DB_PASSWORD=senha_forte
DB_NAME=db_fila_hospital
```

---

## 📊 Logs e Monitoramento

* CloudWatch Logs
* Métricas do ECS / EC2
* Alarmes (opcional)

---

## 🔒 Boas Práticas de Segurança

* Banco em subnet privada
* SG restritivos
* IAM com menor privilégio
* Secrets fora do código
* HTTPS com ACM

---

## 🚀 Evoluções Futuras

* AWS Secrets Manager
* CI/CD com GitHub Actions
* Auto Scaling
* WAF

---

## 🔊 Considerações sobre a aplicação implantada na AWS

Esta documentação representa uma **arquitetura completa, profissional e alinhada ao mercado**, demonstrando domínio em:

* AWS Networking
* Docker
* ECS / Fargate
* Segurança em Cloud
* Arquitetura escalável

📄 Ideal para **GitHub, LinkedIn e entrevistas técnicas**.

## 👾 Considerações Finais

Este projeto demonstra a aplicação prática de **desenvolvimento web com Python**, **gestão de filas em tempo real** e **análise de dados**, sendo ideal para:

* Hospitais;
* Clínicas;
* UPAs;
* Qualquer estabelecimento que trabalhe com filas de atendimento.

Ele pode ser facilmente expandido para incluir notificações por SMS, WhatsApp, integração com painéis físicos ou APIs externas.
---
## 📌 Encerramento

Este projeto foi desenvolvido como parte de um processo de aprendizado e prática em desenvolvimento web com **Python** e **Flask**, aplicando conceitos reais de **sistemas**, **filas de atendimento**, **atualização em tempo real** e **análise de dados**.

📂 **Repositório para clonagem:**  
👉 https://github.com/gabrielsilva798/Sistema-de-Fila-de-Atendimento-em-Flask---Projeto_SENAC.git

Agradeço ao **SENAC**, ao **Farol na Quebrada** e à **Serasa Experian** pela oportunidade, apoio e incentivo durante o desenvolvimento deste projeto, que foi fundamental para nosso crescimento **técnico** e **profissional**.
