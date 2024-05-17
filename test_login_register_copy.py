import unittest
from flask import url_for
from flask_testing import TestCase
from application import create_app, db
from application.models import User

class TestLoginRegister(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_registration(self):
        # Access the registration page
        response = self.client.get('/login-register/login_register')
        self.assertEqual(response.status_code, 200)

        # Register a new user
        response = self.client.post(
            '/login-register/login_register',
            data={'username': 'testuser', 'email': 'test@example.com', 'password': 'password123', 'register': True},
            follow_redirects=True
        )
        self.assertIn(b'Registration successful.', response.data)

        # Check if user is registered
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

    def test_duplicate_username_registration(self):
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        # Attempt to register with the same username
        response = self.client.post(
            '/login-register/login_register',
            data={'username': 'testuser', 'email': 'test2@example.com', 'password': 'password123', 'register': True},
            follow_redirects=True
        )
        self.assertIn(b'Username already exists!', response.data)

    def test_login(self):
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        # Log in with correct credentials
        response = self.client.post(
            '/login-register/login_register',
            data={'username': 'testuser', 'password': 'password123', 'login': True},
            follow_redirects=True
        )
        self.assertIn(b'You have been successfully logged in.', response.data)

        # Log in with incorrect credentials
        response = self.client.post(
            '/login-register/login_register',
            data={'username': 'testuser', 'password': 'wrongpassword', 'login': True},
            follow_redirects=True
        )
        self.assertIn(b'Invalid username or password!', response.data)

if __name__ == '__main__':
    unittest.main()
