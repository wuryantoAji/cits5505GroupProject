from flask import Blueprint, render_template
from .models import WordlePuzzle

main_bp = Blueprint('puzzle-list', __name__)

@main_bp.route('/')
def index():
    puzzles = WordlePuzzle.query.all()
    return render_template('puzzle_list.html', puzzles=puzzles)
