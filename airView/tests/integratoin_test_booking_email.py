# integration_test_booking_email.py
import unittest
import os
import json
import sqlite3
from unittest.mock import patch
from flask_testing import TestCase
from environment.app import app
import authentication.operation as auth_ops
import booking.operation as booking_ops
import time
from werkzeug.security import generate_password_hash
import socket

class BookingEmailIntegrationTest(TestCase):
    def create_app(self):
        """
        Setting up testing environment with Flask
        """
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = False  # Enable sending emails
        app.config['DATABASE'] = 'test_appdata.db'
        app.config['JWT_SECRET_KEY'] = '4e19f3de1b8c3d2abe69c857f724f3ba02bde9bb35688d6215043531a2765514'
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
        app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() in ['true', '1', 't']
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

        print("MAIL_SERVER:", app.config['MAIL_SERVER'])
        print("MAIL_PORT:", app.config['MAIL_PORT'])
        print("MAIL_USE_TLS:", app.config['MAIL_USE_TLS'])
        print("MAIL_USERNAME:", app.config['MAIL_USERNAME'])
        print("MAIL_PASSWORD:", app.config['MAIL_PASSWORD'])
        print("MAIL_DEFAULT_SENDER:", app.config['MAIL_DEFAULT_SENDER'])

        return app

    def setUp(self):
        """
        Setting test database and database path configuration
        removing existing database from testing environment
        ensure test isolation and prevent database locking
        """
        self.test_database = self.app.config['DATABASE']
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
        """)

        hashed_password1 = generate_password_hash('password1', method='pbkdf2:sha256', salt_length=16)

        try:
            curr.execute("INSERT OR IGNORE INTO userdata (userid, email, username, password) VALUES (?, ?, ?, ?)", 
                         (1, 'zanxiang.wang@outlook.com', 'user1', hashed_password1))
            curr.execute("INSERT OR IGNORE INTO flights (flightid, flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                         (1, 'FL001', 'St. Louis', 'Chicago', '2024-06-01 09:00:00', '2024-06-01 10:00:00', 'Scheduled', 'A5'))
            curr.execute("INSERT OR IGNORE INTO seat_classes (classid, classname) VALUES (?, ?)", 
                         (1, 'First Class'))
            curr.execute("INSERT OR IGNORE INTO seats (seatid, flightid, seatnumber, classid, price, is_available) VALUES (?, ?, ?, ?, ?, ?)", 
                         (1, 1, '1A', 1, 150.0, 1))
        except sqlite3.IntegrityError:
            pass

        conn.commit()
        conn.close()

        """
        Give 5 retries attempts to log in test user
        use to detect database locking issue
        """
        retries = 5
        for _ in range(retries):
            try:
                login_response = self.client.post('/auth/login', data=json.dumps({
                    'email': 'zanxiang.wang@outlook.com',
                    'password': 'password1'
                }), content_type='application/json')

                self.assertEqual(login_response.status_code, 200, "Login failed during setup")
                self.token = json.loads(login_response.data)['access_token']
                break
            except sqlite3.OperationalError:
                time.sleep(1)
        else:
            self.fail("Database locking issue detected")

        # DNS Resolution Check
        try:
            socket.gethostbyname(app.config['MAIL_SERVER'])
            print("DNS resolution successful")
        except socket.error as e:
            print(f"DNS resolution failed: {e}")

    def tearDown(self):
        """
        remove test database after unit test
        """
        if os.path.exists(self.test_database):
            os.remove(self.test_database)

    def test_booking_email(self):
        """
        Test booking confirmation email
        """
        headers = {'Authorization': f'Bearer {self.token}'}
        sample_booking_data = {
            'username': 'user1',
            'seatNumber': '1A',
            'numLuggage': 1,
            'flightId': 1
        }

        response = self.client.post('/booking/book', data=json.dumps(sample_booking_data), content_type='application/json', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Booking confirmed')

if __name__ == '__main__':
    unittest.main()