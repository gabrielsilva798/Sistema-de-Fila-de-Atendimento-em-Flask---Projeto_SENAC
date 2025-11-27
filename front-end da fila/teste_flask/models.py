from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from database import Base
from datetime import datetime
import enum

class StatusFila(str, enum.Enum):
    aguardando = "aguardando"
    em_atendimento = "em_atendimento"
    finalizado = "finalizado"

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    telefone = Column(String, nullable=True)
    cpf = Column(String, nullable=True)
    classificacao = Column(String, nullable=True)
    status = Column(String, default=StatusFila.aguardando.value)
    chegada = Column(DateTime, default=datetime.now)

class Medico(Base):
    __tablename__ = "medicos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=True)

class Fila(Base):
    __tablename__ = "fila_atendimento"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=True)
    status = Column(String, default=StatusFila.aguardando.value)
    hora_entrada = Column(DateTime, default=datetime.now)
    hora_inicio = Column(DateTime, nullable=True)
    hora_fim = Column(DateTime, nullable=True)
