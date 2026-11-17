from flask import Flask
from dotenv import load_dotenv

from app.config import Config
from app.extensions import db, migrate

def create_app(config_class=Config):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Register all SQLAlchemy models
    from app import models

    migrate.init_app(app, db)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/health/db")
    def database_health():
        from sqlalchemy import text

        db.session.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected",
        }

    return app