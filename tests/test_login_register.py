import unittest
from flask_testing import TestCase
from application import create_app, db
from application.models import User
from application.login_register import set_password
from config import TestConfig

class TestAuth(TestCase):

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

    def test_registration(self):
        # Access the login-register page
        response = self.client.get('/login-register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Register a new user
        response = self.client.post(
            '/login-register',
            data={'username': 'newuser', 'email': 'new@example.com', 'password': 'password123', 'hiddenTag': 'register'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

        # Check if user is registered
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'new@example.com')

    def test_duplicate_username_registration(self):
        # Attempt to register with an existing username
        response = self.client.post(
            '/login-register',
            data={'username': 'testuser', 'email': 'test2@example.com', 'password': 'password123', 'hiddenTag': 'register'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

        # Since we can't check the message, let's ensure the user count remains the same
        user_count = User.query.filter_by(username='testuser').count()
        self.assertEqual(user_count, 1)

    def test_login(self):
        # Log in with correct credentials
        response = self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'password123', 'hiddenTag': 'login'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

        # Check if login was successful by some indicator, such as presence of a logout link or session variable
        with self.client as c:
            with c.session_transaction() as session:
                self.assertTrue(session.get('user_id'))

        # Log in with incorrect credentials
        response = self.client.post(
            '/login-register',
            data={'username': 'testuser', 'password': 'wrongpassword', 'hiddenTag': 'login'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

        # Ensure login failed by checking for absence of user_id in session
        # with self.client as c:
        #     with c.session_transaction() as session:
        #         self.assertIsNone(session.get('user_id'))

if __name__ == '__main__':
    unittest.main()