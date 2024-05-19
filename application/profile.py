# Import modules
from flask import Blueprint, jsonify, session, redirect, json, render_template
from flask_login import current_user, login_required, logout_user
from application.models import User, WordlePuzzle, ScoreTable
from application import db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/<string:username>', methods=['GET'])
def get_profile(username):
    if(current_user.is_anonymous):
        loginStatus = False
        userName = "-"
    else:
        loginStatus = True
        userName = current_user.username
    user = User.query.filter_by(username=username).first()
    if(user is None):
        return redirect('/404')
    solvedPuzzle = get_solved_puzzles(user.user_id)
    createdPuzzle = get_created_puzzles(user.user_id)
    totalScore = user.overall_score
    return render_template('profile.html', profileUsername=user.username, totalscore = totalScore, solvedPuzzle = solvedPuzzle, createdPuzzle = createdPuzzle, isLogin = loginStatus, username = userName)

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login-register')

# fetching puzzles solved by the user
def get_solved_puzzles(user_id):
    userScores = ScoreTable.query.filter_by(user_id=user_id).all()
    puzzleList = []
    for elem in userScores:
        puzzle_id = elem.puzzle_id
        score = ScoreTable.query.filter_by(puzzle_id=puzzle_id, user_id=user_id).first()
        if(elem.score_achieved == score.score_achieved):
            puzzle = WordlePuzzle.query.filter_by(puzzle_id=score.puzzle_id).first()
            puzzleList.append(puzzle)
    result = [{'name': puzzle.puzzle_name, 'id': puzzle.puzzle_id} for puzzle in puzzleList] if puzzleList else []
    return result

# fetching puzzles created by the user
def get_created_puzzles(user_id):
    created_puzzles = WordlePuzzle.query.filter_by(user_id=user_id).all()
    puzzles = [{'name': puzzle.puzzle_name, 'id': puzzle.puzzle_id} for puzzle in created_puzzles] if created_puzzles else []
    return puzzles