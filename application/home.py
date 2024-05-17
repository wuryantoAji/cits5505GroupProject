import os
from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, json
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from datetime import date
from application.models import User, WordlePuzzle
from application import db

bp_home = Blueprint('home', __name__, url_prefix='/home')

@bp_home.route('/', methods=['GET','POST'])
def index():
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

    return render_template('home.html')
