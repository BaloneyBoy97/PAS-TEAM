import sqlite3
import logging
import os
from werkzeug.security import check_password_hash

DATABASE = None  # Initialize DATABASE as None

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def set_database_path(db_path):
    global DATABASE
    DATABASE = db_path

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(email, username, password, is_admin=False):
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
    try:
        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM userdata WHERE email = ?', (email,)).fetchone()
        logger.debug("User retrieved by email: %s", email)
        return user
    except sqlite3.Error as e:
        logger.error("Error retrieving user by email: %s", e)
        return None

def get_user_by_username(username):
    try:
        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM userdata WHERE username = ?', (username,)).fetchone()
        logger.debug("User retrieved by username: %s", username)
        return user
    except sqlite3.Error as e:
        logger.error("Error retrieving user by username: %s", e)
        return None

def check_user_credentials(password, email):
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