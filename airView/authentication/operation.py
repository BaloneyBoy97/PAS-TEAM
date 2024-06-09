import sqlite3
import logging
from flask import session
from werkzeug.security import check_password_hash

# Initialize DATABASE.
DATABASE = None 
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def set_database_path(db_path):
    global DATABASE
    DATABASE = db_path
    logger.debug(f"Database path set to: {DATABASE}")

def get_db_connection():
    """
    Establish database connection
    """
    if DATABASE is None:
        raise ValueError("Database path is not set. Call set_database_path() first.")
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(email, username, password, is_admin=False):
    """
    Takes argument:
        - email
        - username
        - password
        - is_admin (bool)
    Create new user and store user data in appdata.db
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
    Takes email as argument
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
    Takes username as argument.
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
