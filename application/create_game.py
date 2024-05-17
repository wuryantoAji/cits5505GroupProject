import os
from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, json
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from datetime import date
from application.models import User, WordlePuzzle
from application import db
from urllib.parse import quote
from werkzeug.security import generate_password_hash, check_password_hash
from application.login_register import set_password
from flask_login import login_user

bp_create = Blueprint('create-game', __name__, url_prefix='/create-game')


@bp_create.route('/', methods=['GET', 'POST'])
@login_required
def protect():
    #if not current_user.is_authenticated:
    #    return redirect(url_for('/login-register'))
    if request.method == 'GET':
        return get_request()
    elif request.method == 'POST':
        return post_request()
    
def get_request():
    target = request.args.get('target')
    if target == 'home':
        return redirect(url_for('home'))
    elif target == 'puzzle-list':
        return redirect(url_for('puzzle_list'))
    #elif target == 'leaderboard':
    #    return redirect(url_for('leaderboard'))
    elif target == 'create-game':
        return redirect(url_for('create_game'))
    elif target == 'profile':
        return redirect(url_for('profile'))

def post_request():
    game_name = request.form['form_game_name']
    safe_game_name = quote(game_name.replace(" ", "_").lower())
    existing_game = WordlePuzzle.query.filter_by(name=safe_game_name).first()
    if existing_game:
        return "Game name already exists. Please choose a different name."
    else:
        wordle_solution = request.form['form_wordle_solution']
        number_of_attempts = int(request.form['form_number_of_attempts'])
        base_url = request.url_root.rstrip('/')
        game_url = f"{base_url}/{safe_game_name}"

    new_game = WordlePuzzle(
        user_id=current_user.id,
        puzzle_name=game_name,
        puzzle_solution=wordle_solution,
        number_of_attempt=number_of_attempts,
        puzzle_score=100,
        times_played=0,
    )

    db.session.add(new_game)
    db.session.commit()

    return f"Game created: <a href='{game_url}'></a>"