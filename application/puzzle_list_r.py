from flask import Blueprint, render_template, session
from .models import WordlePuzzle
from flask_login import current_user

main_bp = Blueprint('puzzle-list', __name__, url_prefix="/puzzle-list")

@main_bp.route('/')
def index():
    if(current_user.is_anonymous):
        loginStatus = False
        userName = "-"
    else:
        loginStatus = True
        userName = current_user.username
    puzzles = WordlePuzzle.query.all()
    return render_template('puzzle_list.html', puzzles=puzzles, isLogin = loginStatus, username = userName)
