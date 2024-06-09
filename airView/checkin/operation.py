import sqlite3
import datetime
import logging
from flask import jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger(__name__)

DATABASE = None

def set_database_path(db_path):
    global DATABASE
    DATABASE = db_path

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_id(user_id):
    """
    Retrieve user details by user ID.
    """
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM userdata WHERE userid = ?', (user_id,)).fetchone()
    conn.close()
    return user

def get_booked_flight_details(user_id):
    """
    Fetch booked flight details for the user.
    """
    conn = get_db_connection()
    booking = conn.execute('SELECT * FROM bookings WHERE userid = ?', (user_id,)).fetchone()
    conn.close()
    return booking

def get_flight_details(flight_id):
    """
    Fetch flight details based on flight ID.
    """
    conn = get_db_connection()
    flight = conn.execute('SELECT * FROM flights WHERE flightid = ?', (flight_id,)).fetchone()
    conn.close()
    return flight

def check_in_flight(data, user_id):
    """
    Handle the check-in process for a user.

    Parameters:
    - data: JSON payload with flight details
    - user_id: ID of the user checking in

    Return: User request response (message, status code)
    """
    logger.debug(f"Checking in for user_id: {user_id} with data: {data}")
    flight_id = data['flightId']

    # Fetch booking details
    booking = get_booked_flight_details(user_id)
    
    if not booking:
        logger.error(f"No booking found for user_id: {user_id}")
        return {'error': 'No booking found for this user'}, 400

    if booking['flightid'] != flight_id:
        logger.error(f"No booking found for user_id: {user_id} and flight_id: {flight_id}")
        return {'error': 'No booking found for this flight'}, 400

    # Check if already checked in
    if booking['checked_in']:
        logger.error(f"User_id: {user_id} already checked in for flight_id: {flight_id}")
        return {'error': 'Already checked in'}, 400

    # Update booking to reflect check-in
    conn = get_db_connection()
    conn.execute(
        'UPDATE bookings SET checked_in = 1, check_in_time = ? WHERE bookingid = ?',
        (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), booking['bookingid'])
    )
    conn.commit()
    conn.close()

    return {'message': 'Check-in successful'}, 200

def get_user_id_by_username(username):
    """
    Takes username as argument.
    Retrieve a user ID from the database by username.
    """
    try:
        with get_db_connection() as conn:
            user_id = conn.execute('SELECT userid FROM userdata WHERE username = ?', (username,)).fetchone()
        if user_id:
            logger.debug("User ID retrieved for username: %s", username)
            return user_id[0]  # Return the user ID (assuming it's the first column)
        else:
            logger.debug("No user found for username: %s", username)
            return None
    except sqlite3.Error as e:
        logger.error("Error retrieving user ID by username: %s", e)
        return None
    
# Function to fetch booked flights for a user
def get_booked_flights(username):
    try:
        if username:
            user_id = get_user_id_by_username(username)
            if user_id is not None:
                with get_db_connection() as conn:
                    booked_flights = conn.execute("SELECT * FROM bookings WHERE userid=?", (user_id,)).fetchone()
                    if booked_flights:
                        logger.debug("User retrieved by flights: %s", booked_flights)
                    else:
                        logger.debug("No booked flights found for user with ID: %s", user_id)
            else:
                logger.error("No user found for username: %s", username)
            return user_id, booked_flights
        else:
            logger.error("No username found in session.")
            return None, None
    except sqlite3.Error as e:
        logger.error("Error : %s", e)
        return None,None
    
def get_flight_details(flight_id):
    """
    Fetch flight details based on flight ID.
    """
    try:
        with get_db_connection() as conn:
            flight_details = conn.execute("SELECT * FROM flights WHERE flightid=?", (flight_id,)).fetchone()
        logger.debug("Flight details retrieved by flight ID: %s", flight_id)
        return flight_details
    except sqlite3.Error as e:
        logger.error("Error retrieving flight details by flight ID: %s", e)
        return None
    
def get_user_details(user_id):
    """
    Fetch user details based on user ID.
    """
    try:
        with get_db_connection() as conn:
            user_details = conn.execute("SELECT * FROM userdata WHERE userid=?", (user_id,)).fetchone()
        logger.debug("User details retrieved by user ID: %s", user_id)
        return user_details
    except sqlite3.Error as e:
        logger.error("Error retrieving user details by user ID: %s", e)
        return None
    
def check_in(user_id):
    try:
        database_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
        os.makedirs(database_dir, exist_ok=True)

        db_path = os.path.join(database_dir, 'appdata.db')

        conn = sqlite3.connect(db_path)
        curr = conn.cursor()

        if user_id:
            curr.execute("UPDATE bookings SET is_checked_in = ? WHERE userid = ?", (1, user_id))
            conn.commit()
            conn.close()  # Close the connection
            return {'message': 'Check-in successful'}
        else:
            conn.close()  # Close the connection
            return {'message': 'User ID not provided'}, 400
    except Exception as e:
        return {'message': str(e)}, 500