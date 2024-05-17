import os
from flask import Blueprint, Flask, request, current_app,render_template, session, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_session import Session 

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    #new
    login_manager.init_app(app)
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    @login_manager.user_loader
    def load_user(user_id):
        from application.models import User
        return User.query.get(int(user_id))

    # Import blueprints
    # Register blueprints
    from . import puzzle_list_r
    app.register_blueprint(puzzle_list_r.main_bp)
    from . import play_game
    app.register_blueprint(play_game.bp)
    from . import create_game
    app.register_blueprint(create_game.bp_create)
    from . import login_register
    app.register_blueprint(login_register.bp)
    login_manager.login_view = 'login-register.login_register' 
    from . import home
    app.register_blueprint(home.bp_home)
    # 404 Error Handler
    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404
    
    @app.route('/login-register', methods=['POST'])
    def login():
        # 假设验证用户名和密码成功后
        user_id = 1  # 假设用户ID为1
        session['user_id'] = user_id
        return redirect(url_for('home'))

    @app.route('/')
    def index():
        user_id = session.get('user_id')
        if user_id:
            # 如果用户已经登录，根据用户ID加载用户信息
            user = User.query.get(user_id)
            return render_template('index.html', user=user)
        return render_template('index.html')

    return app