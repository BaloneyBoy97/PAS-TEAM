import unittest
from unittest.mock import patch
from admin.feature import create_flight, update_flight, delete_flight
from admin.operation import get_all_flights

class TestAdminFeature(unittest.TestCase):

    @patch('admin.operation.get_db_connection')
    def test_create_flight_success(self, mock_get_db_connection):
        # Mock the behavior of get_db_connection to return a MagicMock object
        mock_conn = mock_get_db_connection.return_value
        mock_conn.execute.return_value.fetchone.return_value = (1,)  # Adjust mock behavior as per your actual database interaction

        # Your test case logic here
        result = create_flight('FL123', 'Origin', 'Destination', '10:00', '12:00', 'Scheduled', 'Gate 1')
        
        # Assertions based on the expected behavior
        self.assertEqual(result['message'], 'Flight and seats created successfully')

    @patch('admin.operation.get_db_connection')
    def test_delete_flight_success(self, mock_get_db_connection):
        # Mock the behavior of get_db_connection
        mock_conn = mock_get_db_connection.return_value
        mock_execute = mock_conn.execute.return_value
        
        # Simulate a successful deletion
        delete_result = delete_flight(1)  # Assuming flight_id 1 exists
        
        # Assertions based on the expected behavior
        self.assertIsNotNone(delete_result)
        self.assertIn('message', delete_result)
        self.assertEqual(delete_result['message'], 'Flight deleted successfully')

    @patch('admin.operation.get_db_connection')
    def test_update_flight_success(self, mock_get_db_connection):
        # Mock the behavior of get_db_connection
        mock_conn = mock_get_db_connection.return_value
        mock_execute = mock_conn.execute.return_value
        
        # Your test case logic here
        update_result = update_flight(1, 'FL123', 'New Origin', 'New Destination', '11:00', '13:00', 'Delayed', 'Gate 2')
        
        # Assertions based on the expected behavior
        self.assertEqual(update_result, None)  # Assuming update_flight returns None on success

    @patch('admin.operation.get_db_connection')
    def test_update_flight_failure(self, mock_get_db_connection):
        # Mock the behavior of get_db_connection to raise an exception
        mock_conn = mock_get_db_connection.return_value
        mock_conn.execute.side_effect = Exception('Database connection error')
        
        # Your test case logic here
        update_result = update_flight(1, 'FL123', 'New Origin', 'New Destination', '11:00', '13:00', 'Delayed', 'Gate 2')
        
        # Assertions based on the expected behavior
        self.assertIsNone(update_result)  # Assuming update_flight returns None on failure

class TestAdminOperation(unittest.TestCase):

    @patch('admin.operation.get_db_connection')
    def test_get_all_flights(self, mock_get_db_connection):
        # Mock the behavior of get_db_connection to return a MagicMock object
        mock_conn = mock_get_db_connection.return_value
        mock_cursor = mock_conn.execute.return_value
        mock_cursor.fetchall.return_value = [(1, 'FL123', 'Origin', 'Destination', '10:00', '12:00', 'Scheduled', 'Gate 1')]
        
        # Your test case logic here
        flights = get_all_flights()
        
        # Assertions based on the expected behavior
        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0][1], 'FL123')  # Access flightnumber using index

if __name__ == '__main__':
    unittest.main()
