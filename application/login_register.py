from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user
from application.models import User
from application import db

bp = Blueprint('login-register', __name__, url_prefix='/login-register')

@bp.route('/', methods=['GET', 'POST'])
def login_register():
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