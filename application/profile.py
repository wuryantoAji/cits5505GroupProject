# Import modules
from flask import Blueprint, jsonify, session, redirect, json, render_template
from application.models import User, WordlePuzzle, ScoreTable
from application import db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/<string:username>', methods=['GET'])
def get_profile(username):
    try:
        user = session['user_id']
        loginStatus = True
    except KeyError:
        loginStatus = False
    user = User.query.filter_by(username=username).first()
    if(user is None):
        return redirect('/404')
    solvedPuzzle = get_solved_puzzles(user.user_id)
    createdPuzzle = get_created_puzzles(user.user_id)
    totalScore = user.overall_score
    resultPayload = json.dumps({
        'username' : user.username,
        'user_score' : totalScore,
        'solved_puzzle' : solvedPuzzle,
        'created_puzzle' : createdPuzzle,
    })
    return render_template('profile.html', username=user.username, totalscore = totalScore, solvedPuzzle = solvedPuzzle, createdPuzzle = createdPuzzle, isLogin = loginStatus)


# fetching puzzles solved by the user
def get_solved_puzzles(user_id):
    userScores = ScoreTable.query.filter_by(user_id=user_id).all()
    puzzleList = []
    for elem in userScores:
        puzzle_id = elem.puzzle_id
        puzzle = WordlePuzzle.query.filter_by(puzzle_id=puzzle_id, user_id=user_id).first()
        if(elem.score_achieved == puzzle.puzzle_score):
            puzzleList.append(puzzle)
    result = [{'name': puzzle.puzzle_name, 'id': puzzle.puzzle_id} for puzzle in puzzleList] if puzzleList else []
    return result

# fetching puzzles created by the user
def get_created_puzzles(user_id):
    created_puzzles = WordlePuzzle.query.filter_by(user_id=user_id).all()
    puzzles = [{'name': puzzle.puzzle_name, 'id': puzzle.puzzle_id} for puzzle in created_puzzles] if created_puzzles else []
    return puzzles