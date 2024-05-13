import os
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json,
    login_required, current_user
)
from datetime import date
from application.models import User, WordlePuzzle
from application import db

bp_create = Blueprint('create-game', __name__, url_prefix='/create-game')

@bp_create.route('/')
def index():
    return render_template('create_game.html')

@bp_create.route('/create_game', methods=['POST'])
@login_required
def create_game():
    game_name = request.form['form_game_name']
    wordle_solution = request.form['form_wordle_solution']
    number_of_attemps = int(request.form['form_number_of_attemps'])
    #safe_game_name = quote(game_name.replace(" ", "-").lower())
    #game_url = f"{base_url}{safe_game_name}"
    
    new_game = WordlePuzzle(
        user_id=current_user.id,
        puzzle_name=game_name, 
        puzzle_solution=wordle_solution,
        number_of_attempt=number_of_attemps,
        puzzle_score=100,
        times_played=0,
    )

    db.session.add(new_game)
    db.session.commit()
    
    return f"Game created: <a href='{game_url}'> </a>"
