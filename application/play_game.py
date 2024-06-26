import os
import math
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json, redirect
)
from flask_login import current_user
from datetime import date
from application.models import User, WordlePuzzle, ScoreTable
from application import db

bp = Blueprint('play-game', __name__, url_prefix='/play-game')

@bp.route('/<string:puzzleName>', methods=['GET','POST'])
def playGame(puzzleName):
    if(current_user.is_anonymous):
        loginStatus = False
        userName = "-"
    else:
        loginStatus = True
        userName = current_user.username
    gameBoard = WordlePuzzle.query.filter_by(puzzle_name=puzzleName).first()
    if(gameBoard is None):
        return redirect('/404')
    puzzleName = gameBoard.puzzle_name.replace("-"," ")
    puzzlePayload = json.dumps({
        'puzzle_name' : puzzleName,
        'solution_length' : len(gameBoard.puzzle_solution),
        'number_of_guess' : gameBoard.number_of_attempt,
        'score' : gameBoard.puzzle_score,
        'puzzle_id': gameBoard.puzzle_id  
    })
    return render_template('play_game.html',puzzle=puzzlePayload, isLogin = loginStatus, username=userName)

@bp.route('/submit-puzzle-answer/', methods=['POST'])
def submitAnswer():
    if(current_user.is_anonymous):
        loginStatus = False
    else:
        loginStatus = True
    dataPayload = request.get_json()
    puzzleId = dataPayload['puzzleID']
    guess = dataPayload['guess']
    if(any(char.isdigit() for char in guess)):
        return("No Number is Allowed")
    remainingGuessByClient = dataPayload['remainingGuess']
    gameBoard = WordlePuzzle.query.filter_by(puzzle_id=puzzleId).first()
    solution = gameBoard.puzzle_solution
    if(len(guess) != len(solution)):
        return("Not Enough Letter")
    result = []
    isSolved = True
    saveToDB = True
    if (guess == solution):
        for elem in range(len(guess)):
            result.append(2)
    else:
        for index, letter in enumerate(guess):
            if(letter in solution):
                if(solution[index] == guess[index]):
                    result.append(2)
                else:
                    result.append(1)
            else:
                result.append(0)
        isSolved = False
        if(remainingGuessByClient > 0):
            saveToDB = False
    # check if login
    if(loginStatus):
        user = User.query.filter_by(user_id=current_user.user_id).first()
        if(isSolved):
            scoreData = ScoreTable.query.filter_by(user_id=current_user.user_id, puzzle_id=puzzleId).first()
            if(scoreData is None):
                scoreData = ScoreTable(user_id=current_user.user_id, puzzle_id=puzzleId, number_of_attempts=1, score_achieved=gameBoard.puzzle_score)
                db.session.add(scoreData)
            else:
                scoreData.score_achieved = gameBoard.puzzle_score
                scoreData.number_of_attempts += 1
            user.overall_score = user.overall_score + gameBoard.puzzle_score
            flash("You guess it right!!", 'info')
            gameBoard.times_puzzle_played += 1
        else:
            if(saveToDB):
                scoreData = ScoreTable.query.filter_by(user_id=current_user.user_id, puzzle_id=puzzleId).first()
                achievedScore = calculateScore(gameBoard.puzzle_score,result)
                if(scoreData is None):
                    scoreData = ScoreTable(user_id=current_user.user_id, puzzle_id=puzzleId, number_of_attempts=1, score_achieved=achievedScore) 
                    db.session.add(scoreData)
                else:
                    scoreData.number_of_attempts += 1
                    if(achievedScore > scoreData.score_achieved):
                        scoreData.score_achieved = achievedScore
                user.overall_score = user.overall_score + achievedScore
                flash("You ran out of guess attempt.", 'info')
                gameBoard.times_puzzle_played += 1
        db.session.commit()
    resultPayload = json.dumps({"puzzleGuess":result,
                                "solved":isSolved})
    return resultPayload

def calculateScore(puzzleScore, arrayResult):
    worthPerLetter = math.ceil(puzzleScore/len(arrayResult))
    worthPartiallyPerLetter = math.ceil((puzzleScore/len(arrayResult))/2)
    result = 0
    for elem in arrayResult:
        if(elem == 1):
            result = result + worthPartiallyPerLetter
        elif(elem == 2):
            result = result + worthPerLetter
    return result
