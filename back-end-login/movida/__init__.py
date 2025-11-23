from flask import Flask 
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .models import carregar_usuario

load_dotenv()

bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY_FORM")

    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login_paciente"

    login_manager.user_loader(carregar_usuario)

    from .routes import init_routes
    init_routes(app)

    return app

