import unittest
from unittest.mock import patch
from flask import Flask
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flightsearch.feature import flights_bp

class FlightSearchTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(flights_bp, url_prefix='/flights')
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    # To verify that the flight search feature works correctly when given valid input.
    def test_search_flights_success(self):
        # Mocking the get_flights function
        with patch('flightsearch.feature.get_flights') as mock_get_flights:
            # Setting the mock to return a predefined value
            mock_get_flights.return_value = [{'flightnumber': 'ABC123', 'origin': 'JFK', 'destination': 'LAX', 'departuretime': '2024-06-15 09:00:00', 'arrivaltime': '2024-06-15 12:00:00', 'status': 'On time', 'gate_number': 'A1'}]
            
            # Making a GET request to the endpoint
            response = self.client.get('/flights/search?departure=JFK&destination=LAX&departure-date=2024-06-15')
            
            # Assertions to check if the response is as expected
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [{'flightnumber': 'ABC123', 'origin': 'JFK', 'destination': 'LAX', 'departuretime': '2024-06-15 09:00:00', 'arrivaltime': '2024-06-15 12:00:00', 'status': 'On time', 'gate_number': 'A1'}])
    
     
    #To verify that the flight search feature handles missing parameters correctly.
    def test_search_flights_missing_parameters(self):
        # Making a GET request without required parameters
        response = self.client.get('/flights/search')
        
        # Assertions to check if the response is as expected,status code
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Missing required parameters'})

if __name__ == '__main__':
    unittest.main()
