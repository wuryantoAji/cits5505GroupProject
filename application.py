import sqlalchemy as sa
import sqlalchemy.orm as so
from application import app, db
from application.models import User, WordlePuzzle, ScoreTable
from flask_login import LoginManager

