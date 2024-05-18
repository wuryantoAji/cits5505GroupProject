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
    return render_template('./create_game.html')

def get_request():
    target = request.args.get('target')
    if target == 'home':
        return redirect(url_for('home'))
    elif target == 'puzzle-list':
        return redirect(url_for('puzzle_list'))
    elif target == 'leaderboard':
        return redirect(url_for('leaderboard'))
    elif target == 'create-game':
        return redirect(url_for('create_game'))
    elif target == 'profile':
        return redirect(url_for('profile'))
    return render_template('./create_game.html')

def post_request():
    game_name = request.form['form_game_name']
    safe_game_name = quote(game_name.replace(" ", "_").lower())
    existing_game = WordlePuzzle.query.filter_by(puzzle_name=safe_game_name).first()
    if existing_game:
        flash("Game name already exists. Please choose a different name.")
        return render_template('./create_game.html')

    wordle_solution = request.form['form_wordle_solution']
    number_of_attempts = int(request.form['form_number_of_attempts'])
    game_url = f"../play-game/{safe_game_name}"

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

