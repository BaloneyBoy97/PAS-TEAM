import unittest
import os
import sqlite3
from airView.environment.app import app, auth_ops, mail
from unittest.mock import patch, Mock
import json
from werkzeug.security import generate_password_hash
from flask_testing import TestCase
import checkin.operation as checkin_ops

class CheckinTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True
        app.config['DATABASE'] = 'test_appdata.db'
        app.config['JWT_SECRET_KEY'] = '4e19f3de1b8c3d2abe69c857f724f3ba02bde9bb35688d6215043531a2765514'
        return app

    def setUp(self):
        self.test_database = app.config['DATABASE']
        auth_ops.set_database_path(self.test_database)
        checkin_ops.set_database_path(self.test_database)  # Ensure checkin operation has the correct database path

        if os.path.exists(self.test_database):
            os.remove(self.test_database)

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
                flightid INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_number TEXT NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                status TEXT NOT NULL,
                gate_number TEXT NOT NULL
            );
        """)

        hashed_password1 = generate_password_hash('password1', method='pbkdf2:sha256', salt_length=16)
        hashed_password2 = generate_password_hash('password2', method='pbkdf2:sha256', salt_length=16)

        try:
            curr.executemany("INSERT OR IGNORE INTO userdata (userid, email, username, password, isAdmin) VALUES (?, ?, ?, ?, ?)", [
                (1, 'user1@unittest.com', 'user1', hashed_password1, 0),
                (2, 'user2@unittest.com', 'user2', hashed_password2, 0)
            ])
        except sqlite3.IntegrityError:
            pass

        curr.execute("""
            CREATE TABLE IF NOT EXISTS bookings(
                bookingid INTEGER PRIMARY KEY AUTOINCREMENT,
                userid INTEGER,
                flightid INTEGER,
                classid INTEGER,
                seatid INTEGER,
                num_luggage INTEGER,
                booking_time TEXT NOT NULL,
                is_checked_in BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY (userid) REFERENCES userdata(userid),
                FOREIGN KEY (flightid) REFERENCES flights(flightid),
                FOREIGN KEY (classid) REFERENCES seat_classes(classid),
                FOREIGN KEY (seatid) REFERENCES seats(seatid)
            )
        """)

        flights_data = [
            (1, 'FL001', 'Origin1', 'Destination1', '2024-06-01 08:00:00', '2024-06-01 10:00:00', 'Scheduled', 'Gate 1'),
            (2, 'FL002', 'Origin2', 'Destination2', '2024-06-02 09:00:00', '2024-06-02 11:00:00', 'Scheduled', 'Gate 2')
        ]

        curr.executemany("""
            INSERT INTO flights (flightid, flight_number, origin, destination, departure_time, arrival_time, status, gate_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, flights_data)

        bookings_data = [
            (1, 1, 1, 3, 2, 2, '2024-06-02 11:00:00', 0),
            (2, 2, 2, 4, 3, 3, '2024-06-03 12:00:00', 0),
        ]

        curr.executemany("""
            INSERT INTO bookings (bookingid, userid, flightid, classid, seatid, num_luggage, booking_time, is_checked_in)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, bookings_data)

        conn.commit()
        conn.close()

        with patch('authentication.feature.validate_email', return_value=Mock(email='user1@unittest.com')):
            login_response = self.client.post('/auth/login', data=json.dumps({
                'email': 'user1@unittest.com',
                'password': 'password1'
            }), content_type='application/json')

            self.assertEqual(login_response.status_code, 200, "Login failed during setup")
            self.token = json.loads(login_response.data)['access_token']

    def tearDown(self):
        if os.path.exists(self.test_database):
            os.remove(self.test_database)

    @patch('checkin.operation.mail.send', Mock())
    def test_checkin_updates_database(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.post('/checkin/check-in', json={'flight_id': 1}, headers=headers)
        self.assertEqual(response.status_code, 200)

        with sqlite3.connect(self.test_database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT is_checked_in FROM bookings WHERE userid = ? AND flightid = ?", (1, 1))
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], 1)

    @patch('checkin.operation.mail.send', Mock())
    def test_successful_checkin_response(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.post('/checkin/check-in', json={'flight_id': 1}, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Check-in successful')

    @patch('checkin.operation.mail.send', Mock())
    def test_failed_checkin_response(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.post('/checkin/check-in', json={}, headers=headers)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Flight ID not provided')

    @patch('checkin.operation.mail.send', Mock())
    def test_unauthorized_access(self):
        response = self.client.post('/checkin/check-in')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()