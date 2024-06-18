import unittest
import os
import sqlite3
from environment.app import app, auth_ops, mail, jwt_required
from unittest.mock import patch, Mock
import json
from werkzeug.security import generate_password_hash

class CheckinTest(unittest.TestCase):
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
        self.test_database = app.config['DATABASE']    #os.path.abspath('test_database.db')
        auth_ops.set_database_path(self.test_database)

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

        """
        Inserting mock data into the bookings table
        """
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

        """
        Inserting mock data into the flights table
        """
        flights_data = [
            (1, 'FL001', 'Origin1', 'Destination1', '2024-06-01 08:00:00', '2024-06-01 10:00:00', 'Scheduled', 'Gate 1'),
            (2, 'FL002', 'Origin2', 'Destination2', '2024-06-02 09:00:00', '2024-06-02 11:00:00', 'Scheduled', 'Gate 2')
        ]

        curr.executemany("""
            INSERT INTO flights (flightid, flight_number, origin, destination, departure_time, arrival_time, status, gate_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, flights_data)

        bookings_data = [
            (1, 1, 2, 3, 2, 2, '2024-06-02 11:00:00', 0),
            (2, 2, 3, 4, 3, 3, '2024-06-03 12:00:00', 0),
        ]

        curr.executemany("""
            INSERT INTO bookings (bookingid, userid, flightid, classid, seatid, num_luggage, booking_time, is_checked_in)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, bookings_data)

        conn.commit()
        conn.close()

    def tearDown(self):
        """
        remove test database after unit test
        """
        if os.path.exists(self.test_database):
            os.remove(self.test_database)

    # def test_checkin_updates_database(self):
    #     """
    #     Test if the check-in functionality updates the database correctly
    #     """
    #     # Your test code goes here
    #     # Make a check-in request to the endpoint
    #     with app.test_client() as client:
    #         response = client.post('/checkin/check-in', json={'user_id': 1})
    #         self.assertEqual(response.status_code, 200)

    #         # Query the database to check if the user's check-in status has been updated
    #         with sqlite3.connect(self.test_database) as conn:
    #             cursor = conn.cursor()
    #             cursor.execute("SELECT is_checked_in FROM bookings WHERE userid = ?", (1,))
    #             result = cursor.fetchone()
    #             self.assertIsNotNone(result)
    #             self.assertEqual(result[0], 1)  # Assuming 'is_checked_in' field should be set to 1 after check-in

    # def test_successful_checkin_response(self):
    #     """
    #     Test if the response to a successful check-in is as expected
    #     """
    #     # Your test code goes here
    #     with app.test_client() as client:
    #         response = client.post('/checkin/check-in', json={'user_id': 1})
    #         self.assertEqual(response.status_code, 200)
    #         data = response.get_json()
    #         self.assertIn('message', data)
    #         self.assertEqual(data['message'], 'Check-in successful')

    # def test_checkin_endpoint_response(self):
    #     """
    #     Test if the check-in endpoint responds correctly to a POST request
    #     """
    #     with app.test_client() as client:
    #         response = client.post('/checkin/check-in', json={'user_id': 1})
    #         self.assertEqual(response.status_code, 200)

    def test_failed_checkin_response(self):
        """
        Test if the response to a failed check-in is as expected
        """
        # Your test code goes here
        with app.test_client() as client:
            # Trying to check-in without providing a user_id
            response = client.post('/checkin/check-in', json={})
            self.assertEqual(response.status_code, 400)
            data = response.get_json()
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'User ID not provided')

    def test_unauthorized_access(self):
        """
        Test if unauthorized access to the check-in endpoint is handled correctly
        """
        # Your test code goes here
        with app.test_client() as client:
            response = client.post('/checkin/check-in')
            self.assertEqual(response.status_code, 415)

if __name__ == '__main__':
    unittest.main()