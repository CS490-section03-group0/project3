# This file was created to test initialization of the databases

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

socketio = SocketIO()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config):
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder=config.STATIC_FOLDER,
        template_folder=config.TEMPLATE_FOLDER,
    )
    app.config.from_object(config)

    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    migrate.init_app(app, db, render_as_batch=True)

    with app.app_context():
        import server.routes as routes

        app.register_blueprint(routes.main_bp)
        app.register_blueprint(routes.user_bp)
        app.register_blueprint(routes.coinflip_bp)
        app.register_blueprint(routes.leaderboard_bp)
        app.register_blueprint(routes.profile_bp)
        app.register_blueprint(routes.ticket_bp)

    return app
