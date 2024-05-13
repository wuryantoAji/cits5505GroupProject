import sqlalchemy as sa
import sqlalchemy.orm as so
from application import app, db
from application.models import User, WordlePuzzle, ScoreTable, Comments
from flask import Flask, request, redirect, url_for, render_template, session
from urllib.parse import quote

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('create_game.html')

@app.route('/create_game', methods=['POST'])
def create_game():
    game_name = request.form['game_name']
    wordle_solution = request.form['wordle_solution']
    max_attempts = request.form['max_attempts']
    
    # URL处理
    base_url = "http://example.com/games/"  # 假设这是游戏基础URL
    safe_game_name = quote(game_name.replace(" ", "-").lower())  # 安全处理游戏名称
    game_url = f"{base_url}{safe_game_name}"  # 构造完整的游戏URL
    
    game = WordlePuzzle(
        name=game_name,
        solution=WordlePuzzle.puzzle_solution,
        max_attempts=WordlePuzzle.number_of_attempt,
        columns=len(solution),
        rows=int(max_attempts),
        times_played=0,
        game_score=100,
    )
    db.session.add(game)
    db.session.commit()
    
    return f"Game created successfully! <a href='{game_url}'>Play Now!</a>"

if __name__ == '__main__':
    app.run(debug=True)
