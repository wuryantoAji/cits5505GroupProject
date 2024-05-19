import unittest
from flask_testing import TestCase
from application import create_app, db
from application.models import User, WordlePuzzle, ScoreTable
from config import TestConfig

class TestProfile(TestCase):

    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        db.create_all()

        # Create a test user)
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.commit()
        
        db.session.add(user)
        user2 = User(username='testfoo', email='foo@example.com')
        user2.set_password('password123')
        db.session.add(user2)
        db.session.commit()

        puzzle = WordlePuzzle(user_id=user2.user_id, puzzle_name='TestGame', puzzle_solution='TEST', number_of_attempt=3, puzzle_score=100, times_puzzle_played=0)
        db.session.add(puzzle)
        db.session.commit()
        
        scoreTable = ScoreTable(user_id=user.user_id, puzzle_id=puzzle.puzzle_id, number_of_attempts=1, score_achieved=100)
        db.session.add(scoreTable)
        db.session.commit()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_profile_login(self):
        # Access the login-register page
        self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'password123', 'hiddenTag': 'login'},
            follow_redirects=True
        )

        # Access the puzzle list page
        response = self.client.get('/profile/testuser')
        
        # Check if the page renders successfully
        self.assertEqual(response.status_code, 200)

    def test_profile_not_login(self):
        # Access the puzzle list page
        response = self.client.get('/profile/testuser')
        
        # Check if the page renders successfully
        self.assertEqual(response.status_code, 200)

    def test_profile_logout(self):
        # Access the login-register page
        self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'password123', 'hiddenTag': 'login'},
            follow_redirects=True
        )

        # Access the puzzle list page
        response = self.client.post('/profile/logout')
        
        # Check if the page renders successfully
        self.assertEqual(response.status_code, 302)

