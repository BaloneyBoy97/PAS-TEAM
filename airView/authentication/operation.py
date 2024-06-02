import sqlite3
import logging
from werkzeug.security import check_password_hash

DATABASE = 'appdata.db'

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
    logger.debug("User retrieved by username: %s", user)  # Add logging statement
    return user

def check_user_credentials(password, email):
    user = get_user_by_email(email)
    if user:
        logger.debug("User found during credential check")
        if check_password_hash(user['password'], password):
            logger.debug("Password matched")
            return True
    logger.debug("Invalid credentials")
    return False
