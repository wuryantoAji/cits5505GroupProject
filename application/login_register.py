from flask import Flask
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, json
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, HiddenField, EmailField)
from wtforms.validators import InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import User
from application import db

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    hiddenTag = HiddenField('hiddenTag', default="login")

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    hiddenTag = HiddenField('hiddenTag', default="register")

bp = Blueprint('login-register', __name__, url_prefix='/login-register')

@bp.route('/', methods=['GET', 'POST'])
def login_register():
    loginForm = LoginForm()
    registerForm = RegisterForm()
    if request.method == 'POST':
        if registerForm.hiddenTag.data == 'register':
            # Signup
            username = registerForm.username.data
            email = registerForm.email.data
            password = registerForm.password.data
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists!','error')
                return redirect(url_for('login-register.login_register'))
            passwordHash = set_password(password)
            new_user = User(username=username, email=email, password_hash=passwordHash, overall_score=0)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful.','message')
            return redirect(url_for('login-register.login_register'))
        elif loginForm.hiddenTag.data == 'login':
            # Login
            username = loginForm.username.data
            password = loginForm.password.data
            user = User.query.filter_by(username=username).first()
            if user and check_password(user.password_hash, password):
                session['user_id'] = user.user_id
                flash('You have been successfully logged in.','message')
                return redirect(url_for('puzzle-list.index'))
            flash('Invalid username or password!','error')
            return redirect(url_for('login-register.login_register')) # add flash or something
    elif request.method == 'GET':
        return render_template('login_register.html', loginForm=loginForm, registerForm=registerForm)

    #developing: strict authentication - protect from XSS/ SQL inject; safety--https; more complex password + reset password; 

def set_password(password):
    return generate_password_hash(password)

def check_password(password_hash, password):
    return check_password_hash(password_hash, password)