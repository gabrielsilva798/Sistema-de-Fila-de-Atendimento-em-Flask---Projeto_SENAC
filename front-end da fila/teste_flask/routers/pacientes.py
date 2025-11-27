from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
from datetime import datetime

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.PacienteOut)
def criar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    novo = models.Paciente(
        nome=paciente.nome,
        telefone=paciente.telefone,
        cpf=paciente.cpf,
        classificacao=paciente.classificacao,
        status="aguardando",
        chegada=datetime.now()
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/", response_model=list[schemas.PacienteOut])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@router.get("/{paciente_id}", response_model=schemas.PacienteOut)
def get_paciente(paciente_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return p
