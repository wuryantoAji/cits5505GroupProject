import os
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField)
from wtforms.validators import InputRequired
from datetime import date
from application.models import User, WordlePuzzle
from application import db

class CreateGameForm(FlaskForm):
    game_name = StringField('GameName', validators=[InputRequired()])
    wordle_solution = StringField('Solution', validators=[InputRequired()])
    number_of_attempt = IntegerField('NumberOfAttempt', validators=[InputRequired()])

bp_create = Blueprint('create-game', __name__, url_prefix='/create-game')

@bp_create.route('/')
def index():
    try:
        createGame = CreateGameForm()
        user = session['user_id']
        loginStatus = True
        return render_template('create_game.html', isLogin = loginStatus, createGame = createGame)
    except KeyError: 
        return redirect('/404')

@bp_create.route('/create_game', methods=['POST'])
def create_game():
    createGame = CreateGameForm()
    user = session['user_id']
    game_name = createGame.game_name.data
    wordle_solution = createGame.wordle_solution.data
    number_of_attemps = createGame.number_of_attempt.data
    safe_game_name = game_name.replace(" ", "-").lower()
    game_url = f"/play-game/{safe_game_name}"
    new_game = WordlePuzzle(
        user_id=user,
        puzzle_name=game_name, 
        puzzle_solution=wordle_solution,
        number_of_attempt=number_of_attemps,
        puzzle_score=100,
        times_puzzle_played=0,
    )

    db.session.add(new_game)
    db.session.commit()
    
    flash(f"{game_url}",'info')
    return redirect(url_for('create-game.index'))
