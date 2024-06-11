import sqlite3
import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from authentication.operation import get_db_connection


def get_flights(departure, destination, departure_date):
    """
    Retrieves flights from the database that match the provided departure,
    destination, and departure date.

    Returns:
        list: A list of dictionaries containing flight details.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT flightid, flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number
    FROM flights
    WHERE origin = ? AND destination = ? AND date(departuretime) = ?
    """
    cursor.execute(query, (departure, destination, departure_date))
    flights = cursor.fetchall()

    conn.close()

    return [dict(flight) for flight in flights]
