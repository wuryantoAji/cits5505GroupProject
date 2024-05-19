import unittest
from flask_testing import TestCase
from application import create_app, db
from application.models import User
from config import TestConfig

class TestLeaderboard(TestCase):

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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_leaderboard_login(self):
        # Access the login-register page
        self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'password123', 'hiddenTag': 'login'},
            follow_redirects=True
        )

        # Access the puzzle list page
        response = self.client.get('/leaderboard/')
        
        # Check if the page renders successfully
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_not_login(self):
        # Access the puzzle list page
        response = self.client.get('/leaderboard/')
        
        # Check if the page renders successfully
        self.assertEqual(response.status_code, 200)
