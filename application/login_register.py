from flask import Flask
from flask_login import login_user
from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, session, json
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, HiddenField, EmailField)
from wtforms.validators import InputRequired
from flask_login import login_user
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
            new_user = User(username=username, email=email, overall_score=0)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful.','message')
            return redirect(url_for('login-register.login_register'))
        
        elif loginForm.hiddenTag.data == 'login':
            # Login
            username = loginForm.username.data
            password = loginForm.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['user_id'] = user.user_id
                flash('You have been successfully logged in.','message')
                return redirect(url_for('puzzle-list.index'))
            flash('Invalid username or password!','error')
            return redirect(url_for('login-register.login_register'))
    elif request.method == 'GET':
        return render_template('login_register.html', loginForm=loginForm, registerForm=registerForm)

  