import unittest
from flask import url_for
from flask_testing import TestCase
from application import create_app, db
from application.models import User, WordlePuzzle

class TestCreateGame(TestCase):
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        return self.client.post(
            '/login-register/login_register',
            data={'username': username, 'password': password},
            follow_redirects=True
        )

    def test_create_game(self):
        # Log in as the test user
        self.login('testuser', 'password123')

        # Send a POST request to create a new game
        response = self.client.post(
            '/create-game/create_game',
            data={
                'form_game_name': 'Test Game',
                'form_wordle_solution': 'TEST',
                'form_number_of_attemps': '3'
            },
            follow_redirects=True
        )

        # Check if game creation was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Game created:', response.data)

        # Check if the game is stored in the database
        game = WordlePuzzle.query.filter_by(puzzle_name='Test Game').first()
        self.assertIsNotNone(game)
        self.assertEqual(game.puzzle_solution, 'TEST')
        self.assertEqual(game.number_of_attempt, 3)

if __name__ == '__main__':
    unittest.main()
