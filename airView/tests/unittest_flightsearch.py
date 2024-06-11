import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flightsearch.feature import flights_bp

class FlightSearchTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(flights_bp, url_prefix='/api')
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_search_flights_success(self):
        with patch('flightsearch.feature.get_flights') as mock_get_flights:
            mock_get_flights.return_value = [{'flightnumber': 'ABC123', 'origin': 'JFK', 'destination': 'LAX', 'departuretime': '2024-06-15 09:00:00', 'arrivaltime': '2024-06-15 12:00:00', 'status': 'On time', 'gate_number': 'A1'}]
            response = self.client.get('/api/search?departure=JFK&destination=LAX&departure-date=2024-06-15')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [{'flightnumber': 'ABC123', 'origin': 'JFK', 'destination': 'LAX', 'departuretime': '2024-06-15 09:00:00', 'arrivaltime': '2024-06-15 12:00:00', 'status': 'On time', 'gate_number': 'A1'}])

    def test_search_flights_missing_parameters(self):
        response = self.client.get('/api/search')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Missing required parameters'})

if __name__ == '__main__':
    unittest.main()
