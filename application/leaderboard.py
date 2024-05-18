from flask import Blueprint, render_template
from application.models import db, WordlePuzzle, User
from sqlalchemy import func, desc


bp_ldboard = Blueprint('leaderboard', __name__, url_prefix="/leaderboard")

@bp_ldboard.route('/')
def ranking():

    users= db.session.query(
        User.username,
        User.overall_score,
    ).order_by(desc(User.overall_score)).limit(5)
    
    return render_template('leaderboard.html', users=users)

