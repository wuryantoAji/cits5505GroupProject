from flask import Blueprint, render_template
from application.models import db, WordlePuzzle, User
from sqlalchemy import func, desc


bp_ldboard = Blueprint('leaderboard', __name__, url_prefix="/leaderboard")

@bp_ldboard.route('/')
def ranking():

    games = db.session.query(
        WordlePuzzle.puzzle_name.label('puzzle_name'),
        WordlePuzzle.scores.label('scores'),
        WordlePuzzle.puzzle_id.label('puzzle_id'),
        User.username.label('username'),
    ).join(User, WordlePuzzle.user_id == User.user_id).order_by(desc(WordlePuzzle.scores)).limit(5).all()

    return render_template('leaderboard.html', games=games)

