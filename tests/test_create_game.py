import unittest
from flask_testing import TestCase
from application import create_app, db
from application.models import User, WordlePuzzle  # Import WordlePuzzle
from application.login_register import set_password
from config import TestConfig

class TestCreateGame(TestCase):
    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        db.create_all()

        # Create a test user
        password_hash = set_password('password123')
        user = User(username='testuser', password_hash=password_hash, email='test@example.com')
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

        # self.login('testuser', 'password123')

        # Log in as the test user
        self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'password123', 'hiddenTag': 'login'},
            follow_redirects=True
        )

        with self.client as c:
            with c.session_transaction() as session:
                user_id = session.get('user_id')  # Get the user ID from the session

        response = self.client.post(
            '/create-game/create_game',
            data={
                'game_name': 'Test Game',
                'wordle_solution': 'TEST',
                'number_of_attempt': 3
            },
            follow_redirects=True
        )

        # Check if game creation was successful
        self.assertEqual(response.status_code, 200)

        # Check if the game is stored in the database
        game = WordlePuzzle.query.filter_by(puzzle_name='Test Game').first()
        self.assertIsNotNone(game)
        self.assertEqual(game.puzzle_solution, 'TEST')
        self.assertEqual(game.number_of_attempt, 3)

if __name__ == '__main__':
    unittest.main()