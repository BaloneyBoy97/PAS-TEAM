#!/usr/bin/env python3
from flask_mail import Message
import sqlite3
import datetime
import os

# create database connection
def get_db_connection():
    DATABASE = os.path.join(os.path.dirname(__file__), '..', 'database', 'appdata.db')
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# check and display available seats in the selected flight seperated by class
def get_available_seats(flight_id):
    conn = get_db_connection()
    seats = conn.execute('SELECT seatid, seatnumber, classid, is_available FROM seats WHERE flightid = ?', (flight_id,)).fetchall()
    conn.close()
    return [dict(seat) for seat in seats]

# create a booking ticket for the selected flight
def booking_flight(data, user_id, mail):
    username = data['username']
    seat_number = data['seatNumber']
    num_luggage = data['numLuggage']
    flight_id = data['flightId']

    # fetching user email for notification
    conn = get_db_connection()
    user = conn.execute('SELECT email FROM userdata WHERE userid = ?', (user_id,)).fetchone()
    if not user:
        conn.close()
        return {'error': 'User not found'}, 400
    user_email = user['email']

    # Fetch seat_id from seat_number and ensure it's available
    seat = conn.execute('SELECT seatid, classid, price, is_available FROM seats WHERE seatnumber = ? AND flightid = ?', (seat_number, flight_id)).fetchone()
    if not seat or not seat['is_available']:
        conn.close()
        return {'error': 'Seat not available'}, 400
    seat_id = seat['seatid']
    class_id = seat['classid']
    seat_price = seat['price']

    # fetch seat class name
    seat_class = conn.execute('SELECT classname FROM seat_classes WHERE classid = ?', (class_id,)).fetchone()
    if not seat_class:
        conn.close()
        return {'error': 'Invalid Class'}, 400
    class_name  = seat_class['classname']

    # set a max cap for luggage per passenger to 4
    if num_luggage > 4:
        conn.close()
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

    return {'message': 'Booking confirmed', 'total_cost': total_cost}