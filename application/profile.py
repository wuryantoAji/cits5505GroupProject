# Import modules
from flask import Blueprint, jsonify, session
from application.models import User, WordlePuzzle, ScoreTable
from application import db

bp = Blueprint('profile', __name__, url_prefix='/profile')

# fetching the username to be displayed on the profile page
@bp.route('/get_username')
def get_username():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            return jsonify(username=user.username)
    return jsonify(username="Guest")

# Guest Not have the following data

# fetching puzzles solved by the user
def get_solved_puzzles():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(puzzles=[])  # Return empty for guests
    user = User.query.get(user_id)
    solved_puzzles = [{'name': puzzle.puzzle_name, 'id': puzzle.puzzle_id} for puzzle in user.puzzles] if user else []
    return jsonify(puzzles=solved_puzzles)

# fetching puzzles created by the user
@bp.route('/get_created_puzzles')
def get_created_puzzles():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(puzzles=[])  # Return empty for guests
    created_puzzles = WordlePuzzle.query.filter_by(user_id=user_id).all()
    puzzles = [{'name': puzzle.puzzle_name, 'id': puzzle.puzzle_id} for puzzle in created_puzzles] if created_puzzles else []
    return jsonify(puzzles=puzzles)

# fetching the user's scores
@bp.route('/get_scores')
def get_scores():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(overall=0, scores=[])  # Return empty for guests
    user = User.query.get(user_id)
    if user:
        scores = [{'game': score.WordlePuzzle.puzzle_name, 'score': score.score_achieved} for score in user.scores]
        return jsonify(overall=user.overall_score, scores=scores)
    return jsonify(overall=0, scores=[])

