from fastapi import FastAPI
from database import engine, Base
from routers import pacientes, fila, medicos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Atendimento - Clínica/UPA")

app.include_router(pacientes.router)
app.include_router(fila.router)
app.include_router(medicos.router)
