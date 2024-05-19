import os
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField)
from wtforms.validators import InputRequired
from datetime import date
from application.models import User, WordlePuzzle
from application import db
from urllib.parse import quote
import re

class CreateGameForm(FlaskForm):
    game_name = StringField('GameName', validators=[InputRequired()])
    wordle_solution = StringField('Solution', validators=[InputRequired()])
    number_of_attempt = IntegerField('NumberOfAttempt', validators=[InputRequired()])

bp_create = Blueprint('create-game', __name__, url_prefix='/create-game')

@bp_create.route('/', methods=['GET', 'POST'])
@login_required
def protect():
    if request.method == 'GET':
        return get_request()
    elif request.method == 'POST':
        return post_request()
    return render_template('./create_game.html', isLogin = True, username=current_user.username)

def get_request():
    return render_template('./create_game.html', isLogin = True, username=current_user.username)

def post_request():
    game_name = request.form['form_game_name']
    safe_game_name = quote(game_name.replace(" ", "-").lower())
    existing_game = WordlePuzzle.query.filter_by(puzzle_name=safe_game_name).first()
    if existing_game:
        flash("Game name already exists. Please choose a different name.")
        return render_template('./create_game.html')
    
    wordle_solution = request.form['form_wordle_solution']
    number_of_attempts = int(request.form['form_number_of_attempts'])
    game_url = f"../play-game/{safe_game_name}"
    
    game_solution_check = re.compile(r'^[a-zA-Z]+$')

    if len(game_name) > 15:
        flash("Game name too long.")
        return render_template('./create_game.html')
    
    if not game_solution_check.match(wordle_solution) or len(wordle_solution) > 15:
        flash("Wordle solution can only use letters and no longer than 15 letters.")
        return render_template('./create_game.html')
    
    if not number_of_attempts > 0:
        flash("Number of attempts no less than 1.")
        return render_template('./create_game.html')

    new_game = WordlePuzzle(
        user_id=current_user.user_id,
        puzzle_name=safe_game_name,
        puzzle_solution=wordle_solution,
        number_of_attempt=number_of_attempts,
        puzzle_score=100,
        times_puzzle_played=0,
    )

    db.session.add(new_game)
    db.session.commit()
      
    return redirect(game_url)

