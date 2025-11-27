Clinica Backend (FastAPI + SQLite)
=================================
Estrutura:
- main.py
- database.py
- models.py
- schemas.py
- routers/
    - __init__.py
    - pacientes.py
    - fila.py
    - medicos.py
- requirements.txt
- .env

Como rodar:
1. (opcional) crie e ative um virtualenv
2. pip install -r requirements.txt
3. uvicorn main:app --reload
4. Abra http://127.0.0.1:8000/docs para testar as rotas.

Observações:
- O projeto usa SQLite (arquivo clinica.db). Para usar outro DB, atualize DATABASE_URL no .env e em database.py.
