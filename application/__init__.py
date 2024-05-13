import os

from flask import Blueprint, Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

from application import models

def create_app(config_class=Config):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import play_game
    app.register_blueprint(play_game.bp)

    from . import create_game
    app.register_blueprint(create_game.bp_create)

    return app