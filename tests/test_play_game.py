import unittest
from flask import json
from flask_testing import TestCase
from application import create_app, db
from application.models import User, WordlePuzzle
from config import TestConfig

class TestPlayGame(TestCase):
    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        db.create_all()

        # Create a test user)
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        # Create a test puzzle for the test user
        user_id = User.query.filter_by(username='testuser').first()
        puzzle = WordlePuzzle(user_id=user_id.user_id, puzzle_name='TestGame', puzzle_solution='TEST', number_of_attempt=3, puzzle_score=100, times_puzzle_played=0)
        db.session.add(puzzle)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        return self.client.post(
            '/login-register/login_register',
            data={'username': username, 'password': password},
            follow_redirects=True
        )

    def test_access_play_game_page(self):
        # Log in as the test user
        self.login('testuser', 'password123')

        # Access the play game page for the test puzzle
        response = self.client.get('/play-game/TestGame', follow_redirects=True)

        # Check if the page renders successfully
        self.assertEqual(response.status_code, 200)

    def test_submit_puzzle_answer_correct(self):
        # Log in as the test user
        self.login('testuser', 'password123')

        self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'password123', 'hiddenTag': 'login'},
            follow_redirects=True
        )

        with self.client as c:
            with c.session_transaction() as session:
                user_id = session.get('user_id')

        # Prepare JSON payload for correct puzzle submission
        payload = {
            'puzzleID': 1,  # Assuming the puzzle ID is 1
            'guess': 'TEST',
            'remainingGuess': 2
        }

        # Send a POST request to submit puzzle answer
        response = self.client.post(
            '/play-game/submit-puzzle-answer/',
            json=payload
        )

        # Check if the response indicates successful submission
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['solved'])  # Check if puzzle is solved

    def test_submit_puzzle_answer_incorrect(self):
        # Log in as the test user
        self.login('testuser', 'password123')

        self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'password123', 'hiddenTag': 'login'},
            follow_redirects=True
        )

        with self.client as c:
            with c.session_transaction() as session:
                user_id = session.get('user_id')

        # Prepare JSON payload for correct puzzle submission
        payload = {
            'puzzleID': 1,  # Assuming the puzzle ID is 1
            'guess': 'abcd',
            'remainingGuess': 2
        }

        # Send a POST request to submit puzzle answer
        response = self.client.post(
            '/play-game/submit-puzzle-answer/',
            json=payload
        )

        # Check if the response indicates successful submission
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['solved'])  # Check if puzzle is solved

    def test_submit_puzzle_answer_incorrect_zero_guess(self):
        # Log in as the test user
        self.login('testuser', 'password123')

        self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'password123', 'hiddenTag': 'login'},
            follow_redirects=True
        )

        with self.client as c:
            with c.session_transaction() as session:
                user_id = session.get('user_id')

        # Prepare JSON payload for correct puzzle submission
        payload = {
            'puzzleID': 1,  # Assuming the puzzle ID is 1
            'guess': 'TOEP',
            'remainingGuess': 0
        }

        # Send a POST request to submit puzzle answer
        response = self.client.post(
            '/play-game/submit-puzzle-answer/',
            json=payload
        )

        # Check if the response indicates successful submission
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['solved'])  # Check if puzzle is solved
