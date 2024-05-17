from flask_login import login_user
from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, session, json
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
        form_type = request.form.get('form_type')
        if form_type == 'register':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user:
                return jsonify(success=False, message='Username already exists!')
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(success=True)
        elif form_type == 'login':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return jsonify(success=True)
            return jsonify(success=False, message='Invalid username or password!')
    return render_template('login_register.html')

