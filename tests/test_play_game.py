import unittest
from flask import url_for, json
from flask_testing import TestCase
from application import create_app, db
from application.models import User, WordlePuzzle, Comments, ScoreTable

class TestPlayGame(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        # Create a test puzzle
        puzzle = WordlePuzzle(
            puzzle_name='Test Puzzle',
            puzzle_solution='TEST',
            number_of_attempt=3,
            puzzle_score=100,
            times_puzzle_played=0
        )
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

    def test_play_game_render(self):
        # Log in as the test user
        self.login('testuser', 'password123')

        # Access the play game page for the test puzzle
        response = self.client.get('/play-game/Test-Puzzle')
        
        # Check if the page renders successfully
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Puzzle', response.data)  # Check if puzzle name is in the response

    def test_submit_puzzle_answer(self):
        # Log in as the test user
        self.login('testuser', 'password123')

        # Prepare JSON payload for puzzle submission
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

if __name__ == '__main__':
    unittest.main()
