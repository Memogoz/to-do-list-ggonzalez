from flask import Flask, session
from flask_session import Session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_dance.contrib.google import make_google_blueprint, google

db = SQLAlchemy()  # Declarar aquí para evitar ciclos

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'  # Almacenar sesiones en archivos locales
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Duración de la sesión
    Session(app)

    load_dotenv()  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDatabase.db'

    db.init_app(app)  # Conecta la base de datos con la aplicación

    # Google OAuth2 Setup
    google_bp = make_google_blueprint(client_id=os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
                                       client_secret=os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'),
                                       redirect_to='google_login')
    app.register_blueprint(google_bp, url_prefix='/')

    from app.routes.tasks import tasks
    app.register_blueprint(tasks)  # Registra el Blueprint

    with app.app_context():
        db.create_all()  # Crea tablas si no existen

    return app

from .models.models import Task, User
