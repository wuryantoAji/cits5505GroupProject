import unittest
from flask_testing import TestCase
from application import create_app, db
from application.models import User, WordlePuzzle  # Import WordlePuzzle
from config import TestConfig

class TestCreateGame(TestCase):
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

    def login(self, username, password):
        return self.client.post(
            '/login-register/login_register',
            data={'username': username, 'password': password},
            follow_redirects=True
        )

    def test_get_create_game_page(self):
        # Log in as the test user
        self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'password123', 'hiddenTag': 'login'},
            follow_redirects=True
        )

        # Access the create game page
        response = self.client.get('/create-game', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_post_create_game(self):
        # Log in as the test user
        self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'password123', 'hiddenTag': 'login'},
            follow_redirects=True
        )

        response = self.client.post(
            '/create-game',
            data={
                'form_game_name': 'Test Game',
                'form_wordle_solution': 'TEST',
                'form_number_of_attempts': 3
            },
            follow_redirects=True
        )
        # Check if game creation was successful

        # Check if the game is stored in the database
        game = WordlePuzzle.query.filter_by(puzzle_name='test-game').first()
        self.assertIsNotNone(game)
        self.assertEqual(game.puzzle_solution, 'TEST')
        self.assertEqual(game.number_of_attempt, 3)

    def test_post_create_duplicate_game(self):
        # Log in as the test user
        self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'password123', 'hiddenTag': 'login'},
            follow_redirects=True
        )

        response1 = self.client.post(
            '/create-game',
            data={
                'form_game_name': 'Test Game',
                'form_wordle_solution': 'TEST',
                'form_number_of_attempts': 3
            },
            follow_redirects=True
        )

        response2 = self.client.post(
            '/create-game',
            data={
                'form_game_name': 'Test Game',
                'form_wordle_solution': 'TEST',
                'form_number_of_attempts': 3
            },
            follow_redirects=True
        )
        
        self.assertEqual(response2.status_code, 200) 