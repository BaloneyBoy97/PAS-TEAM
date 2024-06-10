import sqlite3
import logging
from flask import jsonify, session
import sys
import os
from flask_mail import Message
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize DATABASE.
DATABASE = None 
mail = None
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def set_database_path(db_path):
    global DATABASE
    DATABASE = db_path
    logger.debug(f"Database path set to: {DATABASE}")

def set_mail_instance(mail_instance):
    global mail
    mail = mail_instance

def get_db_connection():
    """
    Establish database connection
    """
    if DATABASE is None:
        raise ValueError("Database path is not set. Call set_database_path() first.")
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
    
# Function to fetch booked flights for a user
def get_booked_flights(user_id):
    try:
        if user_id is not None:
            with get_db_connection() as conn:
                print("I am Inside")
                booked_flights = conn.execute("SELECT * FROM bookings WHERE userid=?", (user_id,)).fetchone()
                if booked_flights:
                    logger.debug("User retrieved by flights: %s", booked_flights)
                else:
                    logger.debug("No booked flights found for user with ID: %s", user_id)
            return booked_flights
        else:
            logger.error("No user found for userid: %s", user_id)
            return None
    except sqlite3.Error as e:
        logger.error("Error : %s", e)
        return None
    
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