from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PacienteBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    classificacao: Optional[str] = None

class PacienteCreate(PacienteBase):
    pass

class PacienteOut(PacienteBase):
    id: int
    status: str
    chegada: datetime

    class Config:
        orm_mode = True

class MedicoBase(BaseModel):
    nome: str
    especialidade: Optional[str] = None

class MedicoCreate(MedicoBase):
    pass

class MedicoOut(MedicoBase):
    id: int

    class Config:
        orm_mode = True

class FilaCreate(BaseModel):
    paciente_id: int
    medico_id: Optional[int] = None

class FilaOut(BaseModel):
    id: int
    paciente_id: int
    medico_id: Optional[int]
    status: str

    class Config:
        orm_mode = True
