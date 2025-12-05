# app/__init__.py
import os
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()

# cria socketio global (será inicializado com o app em create_app)
socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")


def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")

    # Inicializa SocketIO com o app
    socketio.init_app(app)

    # Importa e registra rotas (passando o objeto socketio)
    from .routes import register_routes
    register_routes(app, socketio)

    return app
