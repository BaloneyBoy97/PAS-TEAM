import sqlite3
import logging
import os
from werkzeug.security import check_password_hash

"""
Initialize DATABASE.
Configure logging
"""
DATABASE = None 
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def set_database_path(db_path):
    """
    Ensure all database operation within 
    booking use this database path
    """
    global DATABASE
    DATABASE = db_path

def get_db_connection():
    """
    establish database connection
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(email, username, password, is_admin=False):
    """
    takes argument:
        - email
        - username
        - password
        - is_admin (bool)
    create new user and store user data in appdata.db
    """
    try:
        with get_db_connection() as conn:
            conn.execute(
                'INSERT INTO userdata (email, username, password, isAdmin) VALUES (?, ?, ?, ?)',
                (email, username, password, is_admin)
            )
        logger.info("User created: %s", email)
    except sqlite3.Error as e:
        logger.error("Error creating user: %s", e)

def get_user_by_email(email):
    """
    takes  email as argument
    Retrieve a user from the database by email.
    """
    try:
        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM userdata WHERE email = ?', (email,)).fetchone()
        logger.debug("User retrieved by email: %s", email)
        return user
    except sqlite3.Error as e:
        logger.error("Error retrieving user by email: %s", e)
        return None

def get_user_by_username(username):
    """
    takes username as argument.
    Retrieve a user from the database by username.
    """
    try:
        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM userdata WHERE username = ?', (username,)).fetchone()
        logger.debug("User retrieved by username: %s", username)
        return user
    except sqlite3.Error as e:
        logger.error("Error retrieving user by username: %s", e)
        return None

def check_user_credentials(password, email):
    """
    Take password and email as argument.
    Authenticate user and return True
    if user credentials are valid, else
    return false.
    """
    try:
        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            logger.info("Credentials verified for user: %s", email)
            return True
        else:
            logger.warning("Invalid credentials for user: %s", email)
            return False
    except Exception as e:
        logger.error("Error checking user credentials: %s", e)
        return False


# Function to fetch booked flights for a user
def get_booked_flights(username):
    user = get_user_by_username(username)
    user_id = user[0]
    try:
        with get_db_connection() as conn:
            booked_filghts = conn.execute("SELECT * FROM bookings INNER JOIN flights ON bookings.flightid = flights.flightid WHERE userid=?", (user_id,)).fetchone()
            logger.debug("User retrieved by flights: %s", booked_filghts)
        return booked_filghts
    except sqlite3.Error as e:
        logger.error("Error retrieving user by username: %s", e)
        return None