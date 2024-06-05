import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from environment.app import app  # Import the app and db objects
from authentication.operation import create_user, get_user_by_email, get_user_by_username

class TestUserRegistration(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['MAIL_SUPPRESS_SEND'] = True
        return app



    def test_valid_email_registration(self):
        with self.client:
            response = self.client.post('/register', json={
                'email': 'validemail@example.com',
                'username': 'validuser',
                'password': 'ValidPass123!'
            })
            self.assertEqual(response.status_code, 201)
            self.assertIn('User registered successfully!', response.json['message'])
            user = get_user_by_email('validemail@example.com')
            self.assertIsNotNone(user)
            self.assertFalse(user.is_admin)

    def test_invalid_email_registration(self):
        with self.client:
            response = self.client.post('/register', json={
                'email': 'invalid-email',
                'username': 'invaliduser',
                'password': 'ValidPass123!'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('The email address is not valid. It must have exactly one @-sign.', response.json['message'])

    def test_empty_email_registration(self):
        with self.client:
            response = self.client.post('/register', json={
                'email': '',
                'username': 'emptyemailuser',
                'password': 'ValidPass123!'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('Email, username, or password is empty!', response.json['message'])

    def test_existing_email_registration(self):
        with self.client:
            create_user('existinguser@example.com', 'existinguser', generate_password_hash('password123'))
            response = self.client.post('/register', json={
                'email': 'existinguser@example.com',
                'username': 'newuser',
                'password': 'ValidPass123!'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('User already exists!', response.json['message'])

    def test_existing_username_registration(self):
        with self.client:
            create_user('uniqueuser@example.com', 'existinguser', generate_password_hash('password123'))
            response = self.client.post('/register', json={
                'email': 'anotheruser@example.com',
                'username': 'existinguser',
                'password': 'ValidPass123!'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('User already exists!', response.json['message'])


class TestAdminRegistration(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['MAIL_SUPPRESS_SEND'] = True
        return app



    def test_valid_admin_registration(self):
        with self.client:
            response = self.client.post('/admin/register', json={
                'email': 'adminemail@example.com',
                'username': 'adminuser',
                'password': 'AdminPass123!'
            })
            self.assertEqual(response.status_code, 201)
            self.assertIn('Admin registered successfully!', response.json['message'])
            admin = get_user_by_email('adminemail@example.com')
            self.assertIsNotNone(admin)
            self.assertTrue(admin.is_admin)

    def test_invalid_email_admin_registration(self):
        with self.client:
            response = self.client.post('/admin/register', json={
                'email': 'invalid-admin-email',
                'username': 'adminuser',
                'password': 'AdminPass123!'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('The email address is not valid. It must have exactly one @-sign.', response.json['message'])

    def test_empty_email_admin_registration(self):
        with self.client:
            response = self.client.post('/admin/register', json={
                'email': '',
                'username': 'emptyadminemailuser',
                'password': 'AdminPass123!'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('Email, username, or password is empty!', response.json['message'])

    def test_existing_email_admin_registration(self):
        with self.client:
            create_user('existingadmin@example.com', 'existingadmin', generate_password_hash('password123'), is_admin=True)
            response = self.client.post('/admin/register', json={
                'email': 'existingadmin@example.com',
                'username': 'newadmin',
                'password': 'AdminPass123!'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('User already exists!', response.json['message'])

    def test_existing_username_admin_registration(self):
        with self.client:
            create_user('uniqueadmin@example.com', 'existingadmin', generate_password_hash('password123'), is_admin=True)
            response = self.client.post('/admin/register', json={
                'email': 'anotheruniqueadmin@example.com',
                'username': 'existingadmin',
                'password': 'AdminPass123!'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('User already exists!', response.json['message'])


class TestUserLogin(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['MAIL_SUPPRESS_SEND'] = True
        return app


    def test_valid_login(self):
        with self.client:
            response = self.client.post('/login', json={
                'email': 'loginuser@example.com',
                'password': 'LoginPass123!'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('Logged in!', response.json['message'])
            self.assertIn('access_token', response.json)

    def test_invalid_email_login(self):
        with self.client:
            response = self.client.post('/login', json={
                'email': 'wronguser@example.com',
                'password': 'LoginPass123!'
            })
            self.assertEqual(response.status_code, 401)
            self.assertIn('Invalid email or password!', response.json['error'])

    def test_invalid_password_login(self):
        with self.client:
            response = self.client.post('/login', json={
                'email': 'loginuser@example.com',
                'password': 'WrongPass123!'
            })
            self.assertEqual(response.status_code, 401)
            self.assertIn('Invalid email or password!', response.json['error'])

    def test_empty_email_login(self):
        with self.client:
            response = self.client.post('/login', json={
                'email': '',
                'password': 'LoginPass123!'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('Email or password is empty!', response.json['error'])

    def test_empty_password_login(self):
        with self.client:
            response = self.client.post('/login', json={
                'email': 'loginuser@example.com',
                'password': ''
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('Email or password is empty!', response.json['error'])


class TestUserLogout(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['MAIL_SUPPRESS_SEND'] = True
        return app


    def test_valid_logout(self):
        with self.client:
            response = self.client.post('/login', json={
                'email': 'logoutuser@example.com',
                'password': 'LogoutPass123!'
            })
            access_token = response.json['access_token']

            headers = {'Authorization': f'Bearer {access_token}'}
            response = self.client.post('/logout', headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Logged out successfully!', response.json['message'])

if __name__ == '__main__':
    unittest.main()
