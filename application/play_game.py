import os
import math
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)
from datetime import date
from application.models import User, WordlePuzzle, Comments, ScoreTable
from application import db

bp = Blueprint('play-game', __name__, url_prefix='/play-game')

@bp.route('/<string:puzzleName>', methods=['GET'])
def playGame(puzzleName):
    gameBoard = WordlePuzzle.query.filter_by(puzzle_name=puzzleName).first()
    print(gameBoard)
    if(gameBoard is None):
        return("No Puzzle Found")
    comments = Comments.query.filter_by(puzzle_id=gameBoard.puzzle_id).order_by(Comments.posted_date).all()
    puzzleName = gameBoard.puzzle_name.replace("-"," ")
    puzzlePayload = json.dumps({
        'puzzle_name' : puzzleName,
        'solution_length' : len(gameBoard.puzzle_solution),
        'number_of_guess' : gameBoard.number_of_attempt,
        'score' : gameBoard.puzzle_score,
        'puzzle_id': gameBoard.puzzle_id  
    })
    return render_template('play_game.html',puzzle=puzzlePayload)

@bp.route('/submit-puzzle-answer/', methods=['POST'])
def submitAnswer():
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
    isLogin = True
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
    if(isLogin):
        if(isSolved):
            scoreData = ScoreTable.query.filter_by(user_id=1, puzzle_id=puzzleId).first()
            if(scoreData is None):
                scoreData = ScoreTable(user_id=1, puzzle_id=puzzleId, number_of_attempts=1, score_achieved=gameBoard.puzzle_score)
                db.session.add(scoreData)
            else:
                scoreData.score_achieved = gameBoard.puzzle_score
                scoreData.number_of_attempts += 1
            gameBoard.times_puzzle_played += 1
        else:
            if(saveToDB):
                scoreData = ScoreTable.query.filter_by(user_id=1, puzzle_id=puzzleId).first()
                achievedScore = calculateScore(gameBoard.puzzle_score,result)
                if(scoreData is None):
                    scoreData = ScoreTable(user_id=1, puzzle_id=puzzleId, number_of_attempts=1, score_achieved=achievedScore) 
                    db.session.add(scoreData)
                else:
                    scoreData.number_of_attempts += 1
                    if(achievedScore > scoreData.score_achieved):
                        scoreData.score_achieved = achievedScore
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
