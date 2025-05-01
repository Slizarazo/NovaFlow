import os
import logging
from flask import Flask
from flask_login import LoginManager
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Aplicar la configuración de Config a la app
app.config.from_object(Config)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import routes after app initialization to avoid circular imports
from routes import *

# Import user model for login management
from models import User

@login_manager.user_loader
def load_user(user_id):
    # Find user by ID from our mock data
    # In a real app, this would query the database
    for user in User.USERS:
        if user.id == int(user_id):
            return user
    return None
