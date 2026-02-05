from flask import Flask
import os
from pathlib import Path
from dotenv import load_dotenv
from src.extensions.extension import db
from src.models.model import Student
from src.routes.chatbot_route import chatbot_bp

load_dotenv()

def create_app():
    # Get the src directory path
    src_dir = Path(__file__).parent
    app = Flask(__name__, 
                 template_folder=str(src_dir / 'templates'),
                 static_folder=str(src_dir / 'static'))
    app.register_blueprint(chatbot_bp)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///default.db")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "defaultsecretkey")

    db.init_app(app)


    with app.app_context():
        db.create_all()

    return app