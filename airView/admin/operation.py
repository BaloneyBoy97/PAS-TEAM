import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from authentication.operation import get_db_connection
import random

# Define columns and rows
columns = 'ABCDEF'

# Define seat parameters
rows_per_class = {
    'First Class': 6,
    'Business': 6,
    'Economy Plus': 10,
    'Economy': 24
}

price_ranges = {
    'First Class': (300.00, 400.00),
    'Business': (200.00, 300.00),
    'Economy Plus': (100.00, 200.00),
    'Economy': (50.00, 100.00)
}

classNames = ['First Class', 'Business', 'Economy Plus', 'Economy']
class_id_map = {name: idx + 1 for idx, name in enumerate(classNames)}

def generate_seats(flight_id):
    seats = []
    for name in classNames:
        class_id = class_id_map[name]
        num_rows = rows_per_class[name]
        min_price, max_price = price_ranges[name]
        
        for row in range(1, num_rows + 1):
            for column in columns:
                seat_id = len(seats) + 1
                seat_num = f'{row}{column}'
                price = round(random.uniform(min_price, max_price), 2)
                seats.append((seat_id, flight_id, seat_num, class_id, price, 1))  # Assuming all seats are initially available

    return seats

# Flight Management Operations
def get_all_flights():
    try:
        conn = get_db_connection()
        flights = conn.execute('SELECT * FROM flights').fetchall()
        return flights
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error fetching flights: {str(e)}")
        return []

def create_flight(flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number):
    try:
        conn = get_db_connection()
        
        # Insert flight details into flights table
        conn.execute(
            'INSERT INTO flights (flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number)
        )
        conn.commit()
        
        # Get the flight_id of the newly inserted flight
        flight_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        # Generate seats for the flight and insert into seats table
        seats = generate_seats(flight_id)
        conn.executemany("INSERT INTO seats (seatid, flightid, seatnumber, classid, price, is_available) VALUES (?, ?, ?, ?, ?, ?)", seats)
        
        conn.commit()
        
        return {"message": "Flight and seats created successfully", "flight_id": flight_id}
    
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error creating flight: {str(e)}")
        return {"error": str(e)}
    
    finally:
        conn.close()

def update_flight(flight_id, flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number):
    try:
        conn = get_db_connection()
        conn.execute(
            'UPDATE flights SET flightnumber = ?, origin = ?, destination = ?, departuretime = ?, arrivaltime = ?, status = ?, gate_number = ? WHERE flightid = ?',
            (flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number, flight_id)
        )
        conn.commit()
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error updating flight: {str(e)}")
    finally:
        conn.close()

def delete_flight(flight_id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM flights WHERE flightid = ?', (flight_id,))
        conn.commit()
        return {"message": "Flight deleted successfully"}
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error deleting flight: {str(e)}")
        return {"error": str(e)}
    finally:
        conn.close()
