import sqlite3
import logging
from flask import jsonify
from flask_mail import Message, Mail
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'database', 'appdata.db') 
mail = Mail()
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
    if DATABASE is None:
        raise ValueError("Database path is not set. Call set_database_path() first.")
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_booked_flights(user_id):
    try:
        conn = get_db_connection()
        curr = conn.cursor()

        if user_id is not None:
            booked_flights = curr.execute("SELECT * FROM bookings WHERE userid=?", (user_id,)).fetchall()
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
    try:
        conn = get_db_connection()
        curr = conn.cursor()

        flight_details = curr.execute("SELECT * FROM flights WHERE flightid=?", (flight_id,)).fetchone()
        logger.debug("Flight details retrieved by flight ID: %s", flight_id)
        return flight_details
    except sqlite3.Error as e:
        logger.error("Error retrieving flight details by flight ID: %s", e)
        return None

def get_user_details(user_id):
    try:
        conn = get_db_connection()
        curr = conn.cursor()

        user_details = curr.execute("SELECT * FROM userdata WHERE userid=?", (user_id,)).fetchone()
        logger.debug("User details retrieved by user ID: %s", user_id)
        return user_details
    except sqlite3.Error as e:
        logger.error("Error retrieving user details by user ID: %s", e)
        return None
def check_in(user_id, flight_id):
    try:
        conn = get_db_connection()
        curr = conn.cursor()

        if user_id and flight_id:
            curr.execute("UPDATE bookings SET is_checked_in = ? WHERE userid = ? AND flightid = ?", (1, user_id, flight_id))
            conn.commit()

            if curr.rowcount > 0:
                # Close connection after commit
                conn.close()

                # Fetch flight details after checking in
                conn = get_db_connection()
                flight_details = get_flight_details(flight_id)
                user_details = get_user_details(user_id)
                conn.close()  # Close connection after fetch

                if flight_details and user_details:
                    user_name = user_details['username']
                    user_email = user_details['email']
                    email_content = f"""
                        <html>
                        <head></head>
                        <body>
                            <p>Dear {user_name},</p>
                            <p>Your check-in for the flight {flight_details['flightnumber']} has been successfully confirmed.</p>
                            <p>Flight Details:</p>
                            <ul>
                                <li>Origin: {flight_details['origin']}</li>
                                <li>Destination: {flight_details['destination']}</li>
                                <li>Departure Time: {flight_details['departuretime']}</li>
                                <li>Arrival Time: {flight_details['arrivaltime']}</li>
                                <li>Status: {flight_details['status']}</li>
                                <li>Gate Number: {flight_details['gate_number']}</li>
                            </ul>
                            <p>Have a pleasant journey!</p>
                        </body>
                        </html>
                    """
                    send_checkin_confirmation_email(user_email, email_content)
                    return {'message': 'Check-in successful'}, 200
                else:
                    return {'message': 'Flight or User details not found'}, 404
            else:
                return {'message': 'No rows updated. User ID or Flight ID not found in bookings.'}, 404
        else:
            return {'message': 'User ID or Flight ID not provided'}, 400
    except Exception as e:
        logger.error("Error during check-in: %s", e)
        return {'message': str(e)}, 500

def send_checkin_confirmation_email(email, content):
    try:
        msg = Message(subject="Check-in Confirmation", recipients=[email], html=content)
        mail.send(msg)
        logger.debug("Check-in confirmation email sent to %s", email)
    except Exception as e:
        logger.error("Error sending check-in confirmation email to %s: %s", email, str(e))