
from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.extensions import db, migrate


def create_app(config_class=Config):

    app = Flask(__name__)

    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Configure CORS
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://localhost:5173"]
            }
        }
    )

    # Root endpoint
    @app.get("/")
    def index():
        return jsonify({
            "message": "Welcome to ReleaseGuard AI API",
            "status": "running"
        }), 200

    # API health check
    @app.get("/api/v1/health")
    def health_check():
        return jsonify({
            "status": "healthy",
            "application": "releaseguard-api"
        }), 200

    # Database health check
    @app.get("/api/v1/health/db")
    def database_health():
        from sqlalchemy import text

        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    return app
