from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
from datetime import datetime

router = APIRouter(prefix="/fila", tags=["fila"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/entrar", response_model=schemas.FilaOut)
def entrar_fila(item: schemas.FilaCreate, db: Session = Depends(get_db)):
    # cria registro na fila e atualiza status do paciente
    paciente = db.query(models.Paciente).filter(models.Paciente.id == item.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    registro = models.Fila(
        paciente_id=item.paciente_id,
        medico_id=item.medico_id,
        status="aguardando",
        hora_entrada=datetime.now()
    )
    paciente.status = "aguardando"
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro

@router.get("/aguardando")
def aguardando(db: Session = Depends(get_db)):
    items = db.query(models.Fila).filter(models.Fila.status == "aguardando").all()
    return items

@router.post("/chamar/{fila_id}")
def chamar(fila_id: int, db: Session = Depends(get_db)):
    fila = db.query(models.Fila).filter(models.Fila.id == fila_id).first()
    if not fila:
        raise HTTPException(status_code=404, detail="Registro da fila não encontrado")
    fila.status = "em_atendimento"
    fila.hora_inicio = datetime.now()
    # atualiza paciente também
    paciente = db.query(models.Paciente).filter(models.Paciente.id == fila.paciente_id).first()
    if paciente:
        paciente.status = "em_atendimento"
    db.commit()
    return {"mensagem": "Paciente em atendimento", "fila": fila.id}

@router.post("/finalizar/{fila_id}")
def finalizar(fila_id: int, db: Session = Depends(get_db)):
    fila = db.query(models.Fila).filter(models.Fila.id == fila_id).first()
    if not fila:
        raise HTTPException(status_code=404, detail="Registro da fila não encontrado")
    fila.status = "finalizado"
    fila.hora_fim = datetime.now()
    paciente = db.query(models.Paciente).filter(models.Paciente.id == fila.paciente_id).first()
    if paciente:
        paciente.status = "finalizado"
    db.commit()
    return {"mensagem": "Atendimento finalizado", "fila": fila.id}
