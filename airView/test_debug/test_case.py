import unittest
from flask import Flask
from flask_testing import TestCase
from app import app  # Import your Flask app
from flask_mail import Mail

class TestUserRegistration(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True
        app.config['MAIL_DEFAULT_SENDER'] = 'noreply@example.com'
        self.mail = Mail(app)
        return app

    def test_registration_with_valid_email(self):
        response = self.client.post('/register', json={
            'email': 'validemail@example.com',
            'username': 'validuser',
            'password': 'validpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully!', response.json['message'])

    def test_registration_with_invalid_email(self):
        response = self.client.post('/register', json={
            'email': 'invalidemail.com',
            'username': 'invaliduser',
            'password': 'validpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('The email address is not valid', response.json['message'])

    def test_registration_with_empty_fields(self):
        response = self.client.post('/register', json={
            'email': '',
            'username': 'emptyuser',
            'password': 'emptypassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email, username, or password is empty!', response.json['message'])

if __name__ == '__main__':
    unittest.main()
