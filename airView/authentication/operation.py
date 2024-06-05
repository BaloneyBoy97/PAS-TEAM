import sqlite3
import logging
import os

# Get the current directory of the script
current_dir = os.path.dirname(__file__)

# Construct the full path to the database file
DATABASE = os.path.join(current_dir, '..', 'database', 'appdata.db')

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(email, username, password, is_admin=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO userdata (email, username, password, isAdmin) VALUES (?, ?, ?, ?)',
        (email, username, password, is_admin)
    )
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM userdata WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    logger.debug("User retrieved by email: %s", user)  # Add logging statement
    return user

def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM userdata WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def check_user_credentials(password, email):
    logger.debug("password: %s", password)
    user = get_user_by_email(email)
    if user:
        logger.debug("User found during credential check")
        logger.debug("Hashed password retrieved from database: %s", user[3])
        logger.debug("password retrieved from user: %s", password)
        if (user and check_user_credentials(user[3], password)):
            logger.debug("Password matched")
            return True
    logger.debug("Invalid credentials")
    return False
