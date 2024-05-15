import unittest
from flask import current_app
from flask_testing import TestCase
from application import create_app, db
from application.models import User

class TestAuth(TestCase):
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

    def test_login(self):
        response = self.client.post('/login', data={'username': 'testuser', 'password': 'password123'}, follow_redirects=True)
        self.assertIn(b'Welcome, testuser!', response.data)

    def test_invalid_login(self):
        response = self.client.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_logout(self):
        self.client.post('/login', data={'username': 'testuser', 'password': 'password123'})
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out', response.data)

    def test_access_control(self):
        response = self.client.get('/profile', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_registration(self):
        response = self.client.post('/register', data={'username': 'newuser', 'email': 'newuser@example.com', 'password': 'password123'}, follow_redirects=True)
        self.assertIn(b'Account created successfully', response.data)

if __name__ == '__main__':
    unittest.main()
