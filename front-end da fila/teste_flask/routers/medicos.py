from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

router = APIRouter(prefix="/medicos", tags=["medicos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.MedicoOut)
def criar_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    novo = models.Medico(nome=medico.nome, especialidade=medico.especialidade)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/", response_model=list[schemas.MedicoOut])
def listar_medicos(db: Session = Depends(get_db)):
    return db.query(models.Medico).all()
