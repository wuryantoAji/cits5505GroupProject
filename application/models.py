from datetime import datetime, timezone
from application import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(256))
    overall_score = db.Column(db.Integer)
    puzzles = db.relationship('WordlePuzzle', backref='User', lazy=True)
    scores = db.relationship('ScoreTable', backref='User', lazy=True)
    comments = db.relationship('Comments', backref='User', lazy=True)
    #add
    is_active = db.Column(db.Boolean, default=True)
    def get_id(self):
        return str(self.user_id)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class WordlePuzzle(db.Model):
    puzzle_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    puzzle_name = db.Column(db.String(64), unique=True)
    puzzle_solution = db.Column(db.String(64))
    number_of_attempt = db.Column(db.Integer)
    puzzle_score = db.Column(db.Integer)
    times_puzzle_played = db.Column(db.Integer)
    scores = db.relationship('ScoreTable', backref='WordlePuzzle', lazy=True)
    comments = db.relationship('Comments', backref='WordlePuzzle', lazy=True)

class ScoreTable(db.Model):
    score_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('wordle_puzzle.puzzle_id'), nullable=False)
    number_of_attempts = db.Column(db.Integer)
    score_achieved = db.Column(db.Integer)

class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('wordle_puzzle.puzzle_id'), nullable=False)
    comment_text = db.Column(db.String(256))
    posted_date = db.Column(db.DateTime)
