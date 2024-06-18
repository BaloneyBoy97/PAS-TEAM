# python -m unittest discover -s tests -p "unittest_booking.py"
import unittest
import os
import json
import sqlite3
from unittest.mock import patch, Mock
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from environment.app import app
import authentication.operation as auth_ops
import booking.operation as booking_ops
import time

class BookingTest(TestCase):
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
        removing existing database from testing environment
        ensure test isolation and prevent database locking
        """
        self.test_database = app.config['DATABASE']
        auth_ops.set_database_path(self.test_database)
        booking_ops.set_database_path(self.test_database)
        
        if os.path.exists(self.test_database):
            os.remove(self.test_database)
        
        """
        Mimicking appdata.db create identical db setup
        insert mock data into db for unit test
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
            
            CREATE TABLE IF NOT EXISTS bookings(
                bookingid INTEGER PRIMARY KEY,
                userid INTEGER,
                flightid INTEGER,
                classid INTEGER,
                seatid INTEGER,
                num_luggage INTEGER,
                booking_time TEXT NOT NULL,
                FOREIGN KEY (userid) REFERENCES userdata(userid),
                FOREIGN KEY (flightid) REFERENCES flights(flightid),
                FOREIGN KEY (classid) REFERENCES seat_classes(classid),
                FOREIGN KEY (seatid) REFERENCES seats(seatid)
            );
            
            CREATE TABLE IF NOT EXISTS seat_classes(
                classid INTEGER PRIMARY KEY,
                classname TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS seats(
                seatid INTEGER PRIMARY KEY,
                flightid INTEGER,
                seatnumber TEXT NOT NULL,
                classid INTEGER,
                price REAL,
                is_available BOOLEAN NOT NULL DEFAULT 1,
                FOREIGN KEY (flightid) REFERENCES flights(flightid),
                FOREIGN KEY (classid) REFERENCES seat_classes(classid)
            );
            
            CREATE TABLE IF NOT EXISTS luggage(
                luggageid INTEGER PRIMARY KEY,
                bookingid INTEGER,
                weight REAL NOT NULL,
                free_luggage INTEGER DEFAULT 0,
                paid_luggage INTEGER DEFAULT 0,
                FOREIGN KEY (bookingid) REFERENCES bookings(bookingid)
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

        curr.executemany("INSERT INTO seat_classes (classname) VALUES (?)", [
            ('First Class',), ('Business',), ('Economy Plus',), ('Economy',)
        ])

        curr.executemany("INSERT INTO seats (flightid, seatnumber, classid, price, is_available) VALUES (?, ?, ?, ?, ?)", [
            (1, '1A', 1, 150.0, 1),
            (1, '1B', 1, 170.0, 1),
            (1, '1C', 1, 200.0, 1),
            (2, '1A', 2, 220.0, 1),
            (2, '1B', 2, 100.0, 1),
            (2, '1C', 2, 230.0, 1)
        ])

        conn.commit()
        conn.close()

        """
        Give 5 retries attempts to log in test user
        use to detect database locking issue
        """
        retries = 5
        for _ in range(retries):
            try:
                with patch('authentication.feature.validate_email', return_value=Mock(email='user1@unittest.com')):
                    login_response = self.client.post('/auth/login', data=json.dumps({
                        'email': 'user1@unittest.com',
                        'password': 'password1'
                    }), content_type='application/json')

                    self.assertEqual(login_response.status_code, 200, "Login failed during setup")
                    self.token = json.loads(login_response.data)['access_token']
                    break
            except sqlite3.OperationalError:
                time.sleep(1)
        else:
            self.fail("Database locking issue detected")
    
    def tearDown(self):
        if os.path.exists(self.test_database):
            os.remove(self.test_database)

    @patch('booking.operation.mail.send', Mock())
    def test_get_available_seats(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.get('/booking/available_seats?flight_id=1', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 3)

        response = self.client.get('/booking/available_seats?flight_id=2', headers=headers)
        data2 = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data2), 3)

    @patch('booking.operation.mail.send', Mock())
    def test_not_available_seat(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        sample_booking_data = {
            'username': 'user1',
            'seatNumber': '1A',
            'numLuggage': 1,
            'flightId': 1
        }

        response = self.client.post('/booking/book', data=json.dumps(sample_booking_data), content_type='application/json', headers=headers)
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/booking/book', data=json.dumps(sample_booking_data), content_type='application/json', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Seat not available')

    @patch('booking.operation.mail.send', Mock())
    def test_booking(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        sample_booking_data = {
            'username': 'user1',
            'seatNumber': '1B',
            'numLuggage': 1,
            'flightId': 1
        }

        response = self.client.post('/booking/book', data=json.dumps(sample_booking_data), content_type='application/json', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Booking confirmed')

    @patch('booking.operation.mail.send', Mock())
    def test_luggage_capacity(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        sample_booking_data = {
            'username': 'user1',
            'seatNumber': '1A',
            'numLuggage': 5,
            'flightId': 1
        }
        response = self.client.post('/booking/book', data=json.dumps(sample_booking_data), content_type='application/json', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Maximum number of luggage is 4')

if __name__ == '__main__':
    unittest.main()