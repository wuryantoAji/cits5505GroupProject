import os
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)
from datetime import date
from application.models import User, WordlePuzzle, Comments

bp = Blueprint('play-game', __name__, url_prefix='/play-game')

@bp.route('/<int:puzzleid>', methods=['GET'])
def playGame(puzzleid):
    gameBoard = WordlePuzzle.query.filter_by(puzzle_id=puzzleid).first()
    comments = Comments.query.filter_by(puzzle_id=puzzleid).order_by(Comments.posted_date).all()
    puzzlePayload = json.dumps({
        'puzzle_name' : gameBoard.puzzle_name,
        'solution_length' : len(gameBoard.puzzle_solution),
        'number_of_guess' : gameBoard.number_of_attempt,
        'score' : gameBoard.puzzle_score,
        'puzzle_id': gameBoard.puzzle_id  
    })
    return render_template('play_game.html',puzzle=puzzlePayload)

@bp.route('/submit-puzzle-answer/', methods=['POST']) # Need to Fix
def submitAnswer():
    for x in request.args:
        print(x)
    return request.args
