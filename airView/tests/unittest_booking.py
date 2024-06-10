# python -m unittest discover -s tests -p "unittest_booking.py"
import unittest
import os
import json
import sqlite3
from unittest.mock import patch, Mock
from flask_testing import TestCase
from environment.app import app
import authentication.operation as auth_ops
import booking.operation as booking_ops
import time

class BookingTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True  # Disable sending emails
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

        # copy the db structure from appdata.py to use as testing database with sample data
        curr.executescript("""
            DROP TABLE IF EXISTS userdata;
            DROP TABLE IF EXISTS flights;
            DROP TABLE IF EXISTS bookings;
            DROP TABLE IF EXISTS seat_classes;
            DROP TABLE IF EXISTS seats;
            DROP TABLE IF EXISTS luggage;
            
            CREATE TABLE userdata(
                userid INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                isAdmin BOOLEAN NOT NULL DEFAULT 0
            );
            
            CREATE TABLE flights(
                flightid INTEGER PRIMARY KEY,
                flightnumber TEXT UNIQUE NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                departuretime TEXT NOT NULL,
                arrivaltime TEXT NOT NULL,
                status TEXT NOT NULL,
                gate_number TEXT NOT NULL
            );
            
            CREATE TABLE bookings(
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
            
            CREATE TABLE seat_classes(
                classid INTEGER PRIMARY KEY,
                classname TEXT NOT NULL
            );
            
            CREATE TABLE seats(
                seatid INTEGER PRIMARY KEY,
                flightid INTEGER,
                seatnumber TEXT NOT NULL,
                classid INTEGER,
                price REAL,
                is_available BOOLEAN NOT NULL DEFAULT 1,
                FOREIGN KEY (flightid) REFERENCES flights(flightid),
                FOREIGN KEY (classid) REFERENCES seat_classes(classid)
            );
            
            CREATE TABLE luggage(
                luggageid INTEGER PRIMARY KEY,
                bookingid INTEGER,
                weight REAL NOT NULL,
                free_luggage INTEGER DEFAULT 0,
                paid_luggage INTEGER DEFAULT 0,
                FOREIGN KEY (bookingid) REFERENCES bookings(bookingid)
            );
        """)
        
        # Creating sample data for unit testing
        curr.executemany("INSERT INTO userdata (email, username, password) VALUES (?, ?, ?)", [
            ('user1@unittest.com', 'user1', 'password1'),
            ('user2@unittest.com', 'user2', 'password2')
        ]) # sample user data

        curr.executemany("INSERT INTO flights (flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number) VALUES (?, ?, ?, ?, ?, ?, ?)", [
            ('FL001', 'St. Louis', 'Chicago', '2024-06-01 09:00:00', '2024-06-01 10:00:00', 'Scheduled', 'A5'),
            ('FL002', 'Chicago', 'St. Louis', '2024-06-02 19:00:00', '2024-06-02 20:00:00', 'Scheduled', 'B4')
        ]) # sample flights data

        curr.executemany("INSERT INTO seat_classes (classname) VALUES (?)", [
            ('First Class',), ('Business',), ('Economy Plus',), ('Economy',)
        ]) # sample seat classes

        curr.executemany("INSERT INTO seats (flightid, seatnumber, classid, price, is_available) VALUES (?, ?, ?, ?, ?)", [
            (1, '1A', 1, 150.0, 1),
            (1, '1B', 1, 170.0, 1),
            (1, '1C', 1, 200.0, 0),
            (2, '1A', 2, 220.0, 1),
            (2, '1B', 2, 100.0, 1),
            (2, '1C', 2, 230.0, 1)
        ]) # sample seat data (flight id, price, seat number, availablity)

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
        os.remove(self.DATABASE)

    def test_get_available_seats(self):
        """
        Test case to get available seats for a flight
        """
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.get('/booking/available_seats?flight_id=1', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2) # only 2 seats should be available

        # sending GET request to endpoint '/booking/available_seats' with flight_id = 2 and class_id = 2
        response = self.client.get('/booking/available_seats?flight_id=2&class_id=2')
        data2 = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data2), 3) # only 3 seats should be available

    def test_not_available_seat(self):
        """
        Test case to check booking for a seat that is not available
        """
        headers = {'Authorization': f'Bearer {self.token}'}
        sample_booking_data = {
            'userid': 1,
            'flightid': 1,
            'classid': 1,
            'seatid': 1,
            'num_luggage': 1,
            'email': 'user1@unittest.com',
            'username': 'user1'
        }
        # Initial attempt (should pass)
        response = self.client.post('/booking/book', data=json.dumps(sample_booking_data), content_type='application/json')

        # Attempt to book the same seat again (should not pass)
        response = self.client.post('/booking/book', data=json.dumps(sample_booking_data), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Seat not available')

    def test_booking(self):
        """
        Test case for successful booking
        """
        headers = {'Authorization': f'Bearer {self.token}'}
        sample_booking_data = {
            'userid': 1,
            'flightid': 1,
            'classid': 1,
            'seatid': 1,
            'num_luggage': 1,
            'email': 'user1@unittest.com',
            'username': 'user1'
        }

        # sending a POST request to endpoint /booking/book
        response = self.client.post('/booking/book', data=json.dumps(sample_booking_data), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'confirm Booking!')

    def test_luggage_capacity(self):
        """
        Test case for luggage capacity limit
        """
        headers = {'Authorization': f'Bearer {self.token}'}
        sample_booking_data = {
            'userid': 1,
            'flightid': 1,
            'classid': 1,
            'seatid': 1,
            'num_luggage': 1,
            'email': 'user1@unittest.com',
            'username': 'user1'
        }
        response = self.client.post('/booking/book', data=json.dumps(sample_booking_data), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'exceeds max capacity')

if __name__ == '__main__':
    unittest.main()