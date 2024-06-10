import unittest
import sys
import os
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from environment.app import app  # Import the app and db objects
from authentication.operation import create_user, get_user_by_email, get_user_by_username

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestSignup(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['MAIL_SUPPRESS_SEND'] = True
        return app

    def test_valid_signup(self):
        with self.client:
            response = self.client.post('/register', json={
                'email': 'validemail@gamil.com',
                'username': 'validuser',
                'password': 'ValidPass123!'
            })
            self.assertEqual(response.status_code, 201)
            self.assertIn('User registered successfully!', response.json['message'])
            user = get_user_by_email('validemail@gmail.com')
            self.assertIsNotNone(user)
            self.assertFalse(user.is_admin)

    def test_invalid_email_signup(self):
        with self.client:
            response = self.client.post('/register', json={
                'email': 'invalid-email',
                'username': 'invaliduser',
                'password': 'ValidPass123!'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('The email address is not valid. It must have exactly one @-sign.', response.json['message'])

    def test_empty_email_signup(self):
        with self.client:
            response = self.client.post('/register', json={
                'email': '',
                'username': 'emptyemailuser',
                'password': 'ValidPass123!'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('Email, username, or password is empty!', response.json['message'])

    def test_existing_email_signup(self):
        with self.client:
            create_user('aaaa123@gmail.com', 'existinguser', generate_password_hash('password123'))
            response = self.client.post('/register', json={
                'email': 'john.doe@example.com',
                'username': 'JohnDoe',
                'password': 'password123'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('User already exists!', response.json['message'])

    def test_existing_username_signup(self):
        with self.client:
            create_user('john.doe@example.com', 'existinguser', generate_password_hash('password123'))
            response = self.client.post('/register', json={
                'email': 'john.doe@example.com',
                'username': 'JohnDoe',
                'password': 'password123'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('User already exists!', response.json['message'])

if __name__ == '__main__':
    unittest.main()
