import sqlite3
import os
import sys 
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from authentication.operation import get_db_connection

logger = logging.getLogger(__name__)

def get_flights(departure, destination, departure_date):
    """
    Retrieves flights from the database that match the provided departure,
    destination, and departure date.

    Args:
        departure (str): The departure location.
        destination (str): The destination location.
        departure_date (str): The departure date in 'YYYY-MM-DD' format.

    Returns:
        list: A list of dictionaries containing flight details.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT flightid, flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number
        FROM flights
        WHERE origin = ? AND destination = ? AND date(departuretime) = ?
        """
        cursor.execute(query, (departure, destination, departure_date))
        flights = cursor.fetchall()
        
        # Convert each row to a dictionary
        flights_list = [
            {
                "flightid": flight[0],
                "flightnumber": flight[1],
                "origin": flight[2],
                "destination": flight[3],
                "departuretime": flight[4],
                "arrivaltime": flight[5],
                "status": flight[6],
                "gate_number": flight[7]
            } for flight in flights
        ]

        logger.info(f"Retrieved {len(flights_list)} flights from the database.")
        return flights_list

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return []

    finally:
        if conn:
            conn.close()
