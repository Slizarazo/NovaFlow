import os
import logging
from flask import Flask
from flask_login import LoginManager
from config import Config
from datetime import timedelta

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
# app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.secret_key = "nfguofg4ofb"
app.config['SECRET_KEY'] = "nfguofg4ofb"

# Seguridad y manejo de cookies en entorno local
app.config['SESSION_COOKIE_SECURE'] = False  # Permite cookies sin HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Permite que se mantengan en redirecciones
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Seguridad JS
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)


# Aplicar la configuración de Config a la app
# app.config.from_object(Config)

# Inicializar LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import routes after app initialization to avoid circular imports
from routes import *

# Import user model for login management
from models import UserAcces

@login_manager.user_loader
def load_user(user_id):
    print(f"🧠 load_user invocado con ID: {user_id}")
    return UserAcces.get_by_id(user_id)






