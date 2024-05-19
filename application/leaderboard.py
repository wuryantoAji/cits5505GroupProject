from flask import Blueprint, render_template
from application.models import db, User
from sqlalchemy import desc
from flask_login import current_user

bp_ldboard = Blueprint('leaderboard', __name__, url_prefix="/leaderboard")

@bp_ldboard.route('/')
def ranking():
    print("test")
    if(current_user.is_anonymous):
        loginStatus = False
        userName = "-"        
    else:
        loginStatus = True
        userName = current_user.username
    users= db.session.query(
        User.username,
        User.overall_score,
    ).order_by(desc(User.overall_score)).limit(5)
    
    return render_template('leaderboard.html', users=users, isLogin = loginStatus, username=userName)

