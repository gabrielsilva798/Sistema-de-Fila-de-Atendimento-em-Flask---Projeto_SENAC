import os
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()

# Use threading mode on Windows (stable)
socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")

def create_app():
    BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE, "templates"),
        static_folder=os.path.join(BASE, "static")
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "troque_esta_chave")

    # register routes (routes needs socketio)
    from .routes import init_routes
    init_routes(app, socketio)

    socketio.init_app(app)
    return app
