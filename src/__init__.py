from flask import Flask
import os
from dotenv import load_dotenv
from src.extensions.extension import db
from src.models.model import Student
from src.routes.chatbot_route import chatbot_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(chatbot_bp)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///default.db")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "defaultsecretkey")

    db.init_app(app)


    with app.app_context():
        db.create_all()

    return app