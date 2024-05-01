from datetime import datetime, timezone
from application import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(256))
    overall_score = db.Column(db.Integer)
    puzzles = db.relationship('WordlePuzzle', backref='User', lazy=True)
    scores = db.relationship('ScoreTable', backref='User', lazy=True)
    comments = db.relationship('Comments', backref='User', lazy=True)

class WordlePuzzle(db.Model):
    puzzle_id = db.Column(primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    puzzle_name = db.Column(db.String(64), unique=True)
    puzzle_solution = db.Column(db.String(64))
    number_of_attempt = db.Column(db.Integer)
    puzzle_score = db.Column(db.Integer)
    scores = db.relationship('ScoreTable', backref='WordlePuzzle', lazy=True)

class ScoreTable(db.Model):
    score_id = db.Column(primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('WordlePuzzle.puzzle_id'), nullable=False)
    score_achieved = db.Column(db.Integer)

class Comments(db.Model):
    comment_id = db.Column(primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    comment_text = db.Column(db.String(256))
    posted_date = db.Column(db.DateTime)
