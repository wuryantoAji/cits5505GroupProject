import os
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)
from flask_login import LoginManager
from flask_login import login_required, current_user
from datetime import date
from application.models import User, WordlePuzzle
from application import db
from urllib.parse import quote

bp_create = Blueprint('create-game', __name__, url_prefix='/create-game')


def load_user(user_id):
    return User.query.get(int(user_id))

@bp_create.route('/', methods=['GET','POST'])
@login_required
def create_game():
    if request.method == 'GET':
        target = request.args.get('target')
        if target == 'home':
            return redirect(url_for('home'))
        elif target == 'puzzle-list':
            return redirect(url_for('puzzle-list'))
        elif target == 'leaderboard':
            return redirect(url_for('leaderboard'))
        elif target == 'create-game':
            return redirect(url_for('create-game'))
        elif target == 'profile':
            return redirect(url_for('profile'))

    if request.method == 'POST':
        game_name = request.form['form_game_name']
        wordle_solution = request.form['form_wordle_solution']
        number_of_attemps = int(request.form['form_number_of_attemps'])
        safe_game_name = quote(game_name.replace(" ", "-").lower())
        game_url = f"{base_url}{safe_game_name}"
        
        new_game = WordlePuzzle(
            user_id=1,
            puzzle_name=game_name, 
            puzzle_solution=wordle_solution,
            number_of_attempt=number_of_attemps,
            puzzle_score=100,
            times_played=0,
        )

        db.session.add(new_game)
        db.session.commit()
        
        return f"Game created: <a href='{game_url}'> </a>"
