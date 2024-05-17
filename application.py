import sqlalchemy as sa
import sqlalchemy.orm as so
from application import app, db
from application.models import User, WordlePuzzle, ScoreTable, Comments
from flask_login import LoginManager

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return db.User.query.get(user_id)

