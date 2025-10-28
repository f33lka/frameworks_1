import os, logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

from config import Config
from database import db
from models import User, Project, Defect
from auth import bp as auth_bp
from projects import bp as projects_bp
from defects import bp as defects_bp
from reports import bp as reports_bp

load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Allow env override for tests / ops
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", app.config["SQLALCHEMY_DATABASE_URI"])

    # Ensure instance path exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Force absolute SQLite path into instance/app.db for stable Windows runs
    uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if uri.startswith("sqlite:///"):
        rel = uri.replace("sqlite:///", "", 1)
        if not os.path.isabs(rel):
            db_path = os.path.join(app.instance_path, "app.db")
            app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    # DB
    db.init_app(app)

    # JWT
    JWTManager(app)

    # CORS
    CORS(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(defects_bp)
    app.register_blueprint(reports_bp)

    # Health
    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    # Logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    with app.app_context():
        init_db()

    return app