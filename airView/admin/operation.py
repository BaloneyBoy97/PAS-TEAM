import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from authentication.operation import get_db_connection

# Flight Management Operations
def get_all_flights():
    conn = get_db_connection()
    flights = conn.execute('SELECT * FROM flights').fetchall()
    conn.close()
    return flights

def create_flight(flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO flights (flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number)
    )
    conn.commit()
    conn.close()

def update_flight(flight_id, flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number):
    conn = get_db_connection()
    conn.execute(
        'UPDATE flights SET flightnumber = ?, origin = ?, destination = ?, departuretime = ?, arrivaltime = ?, status = ?, gate_number = ? WHERE flightid = ?',
        (flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number, flight_id)
    )
    conn.commit()
    conn.close()

def delete_flight(flight_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM flights WHERE flightid = ?', (flight_id,))
    conn.commit()
    conn.close()
