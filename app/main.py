from datetime import timedelta
import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

from app.models import db
from app.auth import auth
from app.routes import auth_router

app = Flask(__name__)


# Middlewares
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URI', 'sqlite:///notes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


Migrate(app, db)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
auth.init_app(app)


# Routes
app.register_blueprint(auth_router, url_prefix="/api/v1/auth")

if __name__ == '__main__':
    load_dotenv()
    app.run(port=8080)
