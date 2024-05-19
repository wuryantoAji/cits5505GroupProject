import unittest
from flask_testing import TestCase
from application import create_app, db
from application.models import User, WordlePuzzle  # Import WordlePuzzle
from config import TestConfig

class TestPuzzleList(TestCase):
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

    def test_puzzle_list_render(self):
        # Access the puzzle list page
        response = self.client.get('/puzzle-list/')
        
        # Check if the page renders successfully
        self.assertEqual(response.status_code, 200)

