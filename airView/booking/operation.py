import sqlite3
import datetime
from flask_mail import Message
import logging

logger = logging.getLogger(__name__)

DATABASE = None
mail = None

def set_database_path(db_path):
    """
    Ensure all database operation within 
    booking use this database path
    """
    global DATABASE
    DATABASE = db_path

def set_mail_instance(mail_instance):
    """
    Setting mail instance to allow booking
    to set email notification without 
    reinitialize or pass main instance
    """
    global mail
    mail = mail_instance

def get_db_connection():
    """
    establish database connection
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_available_seats(flight_id):
    """
    Check and display available seats 
    Using flight_id as parameter to identify flight
    return a list of dictionary with seat information
    """
    conn = get_db_connection()
    seats = conn.execute('SELECT seatid, seatnumber, classid, is_available FROM seats WHERE flightid = ?', (flight_id,)).fetchall()
    conn.close()
    return [dict(seat) for seat in seats]

def booking_flight(data, user_id):
    """
    create a booking ticket for the selected flight

    parameters:
    username, user_id, seat number, 
    number of luggage, and flight ID

    Return: User request response (message, status code)

    """
    logger.debug(f"Booking flight for user_id: {user_id} with data: {data}")
    username = data['username']
    seat_number = data['seatNumber']
    num_luggage = data['numLuggage']
    flight_id = data['flightId']

    # fetching user email for notification
    conn = get_db_connection()
    user = conn.execute('SELECT email FROM userdata WHERE userid = ?', (user_id,)).fetchone()
    if not user:
        conn.close()
        logger.error(f"User not found for user_id: {user_id}")
        return {'error': 'User not found'}, 400
    user_email = user['email']

    # Fetch seat_id from seat_number and ensure it's available
    seat = conn.execute('SELECT seatid, classid, price, is_available FROM seats WHERE seatnumber = ? AND flightid = ?', (seat_number, flight_id)).fetchone()
    if not seat or not seat['is_available']:
        conn.close()
        logger.error(f"Seat not available for seat_number: {seat_number}, flight_id: {flight_id}")
        return {'error': 'Seat not available'}, 400
    seat_id = seat['seatid']
    class_id = seat['classid']
    seat_price = seat['price']

    # fetch seat class name
    seat_class = conn.execute('SELECT classname FROM seat_classes WHERE classid = ?', (class_id,)).fetchone()
    if not seat_class:
        conn.close()
        logger.error(f"Invalid class for class_id: {class_id}")
        return {'error': 'Invalid Class'}, 400
    class_name = seat_class['classname']

    # set a max cap for luggage per passenger to 4
    if num_luggage > 4:
        conn.close()
        logger.error(f"Number of luggage exceeded for user_id: {user_id}, num_luggage: {num_luggage}")
        return {'error': 'Maximum number of luggage is 4'}, 400
    
    # calculate luggage fees if passenger selected more than 2 luggage to carry
    free_luggage = 2
    extra_luggage_cost = 25.0  # Cost for each extra luggage
    additional_luggage = max(0, num_luggage - free_luggage)
    luggage_cost = additional_luggage * extra_luggage_cost

    total_cost = seat_price + luggage_cost

    # insert booking information
    curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('INSERT INTO bookings (userid, flightid, classid, seatid, num_luggage, booking_time) VALUES (?, ?, ?, ?, ?, ?)',
                 (user_id, flight_id, class_id, seat_id, num_luggage, curr_time))
    conn.execute('UPDATE seats SET is_available = 0 WHERE seatid = ?', (seat_id,))
    conn.commit()

    # Get flight details for email notification
    flight = conn.execute('SELECT * FROM flights WHERE flightid = ?', (flight_id,)).fetchone()
    conn.close()

    msg = Message('Booking Confirmation', recipients=[user_email])
    msg.body = f"""
    Dear {username},

    Your booking has been confirmed.

    Booking Details:
    Flight Number: {flight['flightnumber']}
    Origin: {flight['origin']}
    Destination: {flight['destination']}
    Departure Time: {flight['departuretime']}
    Gate Number: {flight['gate_number']}
    Arrival Time: {flight['arrivaltime']}

    Seat Number: {seat_number}
    Class: {class_name}
    Number of Luggage: {num_luggage}
    Total Cost: ${total_cost:.2f}

    Thank you for choosing AirView!
    """
    mail.send(msg)

    return {'message': 'Booking confirmed', 'total_cost': total_cost}, 200
