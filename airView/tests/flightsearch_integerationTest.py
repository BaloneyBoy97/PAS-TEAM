import unittest
import os
import sys
import json
import sqlite3
from unittest.mock import patch, Mock
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.app import app
import flightsearch.operation as flight_ops
import authentication.operation as auth_ops
import time

class FlightSearchTest(TestCase):
    def create_app(self):
        """
        Setting up testing environment with Flask
        """
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True
        app.config['DATABASE'] = 'test_appdata.db'
        app.config['JWT_SECRET_KEY'] = '4e19f3de1b8c3d2abe69c857f724f3ba02bde9bb35688d6215043531a2765514'
        return app

    def setUp(self):
        """
        Setting test database and database path configuration
        Removing existing database from testing environment
        Ensure test isolation and prevent database locking
        """
        self.test_database = app.config['DATABASE']
        auth_ops.set_database_path(self.test_database)

        if os.path.exists(self.test_database):
            os.remove(self.test_database)

        """
        Mimicking appdata.db create identical db setup
        Insert mock data into db for unit test
        """
        conn = sqlite3.connect(self.test_database)
        curr = conn.cursor()

        curr.executescript("""
            CREATE TABLE IF NOT EXISTS userdata(
                userid INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                isAdmin BOOLEAN NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS flights(
                flightid INTEGER PRIMARY KEY,
                flightnumber TEXT UNIQUE NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                departuretime TEXT NOT NULL,
                arrivaltime TEXT NOT NULL,
                status TEXT NOT NULL,
                gate_number TEXT NOT NULL
            );
        """)

        hashed_password1 = generate_password_hash('password1', method='pbkdf2:sha256', salt_length=16)
        hashed_password2 = generate_password_hash('password2', method='pbkdf2:sha256', salt_length=16)

        try:
            curr.executemany("INSERT OR IGNORE INTO userdata (userid, email, username, password) VALUES (?, ?, ?, ?)", [
                (1, 'user1@unittest.com', 'user1', hashed_password1),
                (2, 'user2@unittest.com', 'user2', hashed_password2)
            ])
        except sqlite3.IntegrityError:
            pass

        curr.executemany("INSERT OR IGNORE INTO flights (flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number) VALUES (?, ?, ?, ?, ?, ?, ?)", [
            ('FL001', 'St. Louis', 'Chicago', '2024-06-01 09:00:00', '2024-06-01 10:00:00', 'Scheduled', 'A5'),
            ('FL002', 'Chicago', 'St. Louis', '2024-06-02 19:00:00', '2024-06-02 20:00:00', 'Scheduled', 'B4')
        ])

        conn.commit()
        conn.close()

        """
        Login test user
        """
        login_response = self.client.post('/auth/login', data=json.dumps({
            'email': 'user1@unittest.com',
            'password': 'password1'
        }), content_type='application/json')

        self.assertEqual(login_response.status_code, 200, "Login failed during setup")
        self.token = json.loads(login_response.data)['access_token']

    def tearDown(self):
        """
        Remove test database after unit test
        """
        if os.path.exists(self.test_database):
            os.remove(self.test_database)

    def test_search_flights_success(self):
        """
        Test case for successful flight search
        """
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.get('/flights/search?departure=St. Louis&destination=Chicago&departure-date=2024-06-01', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['flightnumber'], 'FL001')

    def test_search_flights_missing_parameters(self):
        """
        Test case for missing parameters in flight search
        """
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.get('/flights/search?departure=St. Louis&destination=Chicago', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing required parameters')

    def test_search_flights_no_results(self):
        """
        Test case for no results in flight search
        """
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.get('/flights/search?departure=St. Louis&destination=New York&departure-date=2024-06-01', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()