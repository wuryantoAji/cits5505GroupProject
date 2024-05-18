import os

from flask import Blueprint, Flask, request, current_app, render_template, redirect
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

    # Import blueprints
    from . import puzzle_list_r

    # Register blueprints
    app.register_blueprint(puzzle_list_r.main_bp)

    from . import play_game
    app.register_blueprint(play_game.bp)

    from . import login_register
    app.register_blueprint(login_register.bp)
    from . import create_game
    app.register_blueprint(create_game.bp_create)
    
    from . import profile
    app.register_blueprint(profile.bp)

    # 404 Error Handler
    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404
    
    @app.route("/")
    def default_route():
        return redirect('/login-register')
        

    return app