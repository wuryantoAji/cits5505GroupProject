from flask import Flask
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import User
from application import db

bp = Blueprint('login-register', __name__, url_prefix='/login-register')

@bp.route('/', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        if 'register' in request.form:
            # Signup
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists!')
                return redirect(url_for('auth.login_register'))
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful.')
            return redirect(url_for('auth.login_register'))
        elif 'login' in request.form:
            # Login
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['user_id'] = user.user_id
                flash('You have been successfully logged in.')
                return redirect(url_for('puzzle-list'))
            flash('Invalid username or password!')
    return render_template('login_register.html')

    #developing: strict authentication - protect from XSS/ SQL inject; safety--https; more complex password + reset password; 

def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)