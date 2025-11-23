from flask import Flask
import os
from dotenv import load_dotenv

from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY_FORM")

    from .routes import init_routes
    init_routes(app)

    return app
