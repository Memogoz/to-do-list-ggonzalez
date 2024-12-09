from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()  # Declarar aquí para evitar ciclos

def create_app():
    app = Flask(__name__)

    load_dotenv()  
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    db.init_app(app)  # Conecta la base de datos con la aplicación

    from app.routes.tasks import tasks
    app.register_blueprint(tasks)  # Registra el Blueprint

    with app.app_context():
        db.create_all()  # Crea tablas si no existen

    return app

from app.models import User, Task
