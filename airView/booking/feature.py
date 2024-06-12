from flask import Blueprint, request, jsonify
from flask_mail import Mail
from flask_jwt_extended import jwt_required, get_jwt_identity
from booking.operation import booking_flight, get_available_seats, set_mail_instance
import logging

"""
create booking blueprint to define routes of booking page.
Initialize Mail object for Email Notification.
send mail instance to booking/operation.py for Email operation
"""
booking_bp = Blueprint('booking_bp', __name__)
mail = Mail()
set_mail_instance(mail)

# Configure logging 
logger = logging.getLogger(__name__)

@booking_bp.route('/available_seats', methods=['GET'])
@jwt_required()
def available_seats():
    """
    define endpoint for seats
    user authentication, check for valid web token
    request flight_id as query string
    returns all available seats match fligh_id
    or error message if flight_id is not valid
    """
    flight_id = request.args.get('flight_id')
    if not flight_id:
        return jsonify({'error': 'Null Input'}), 400

    try:
        logger.info(f"Fetching available seats for flight_id: {flight_id}")
        seats = get_available_seats(flight_id)
        return jsonify(seats)
    except Exception as e:
        logger.error(f"Error fetching available seats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/book', methods=['POST'])
@jwt_required()
def book():
    """
    define endpoint for booking
    user authentication, check for valid web token
    JSON payload: (Front End User Input)
        - USERNAME
        - SEAT NUMBER
        - NUMBER OF LUGGAGE
        - FLIGHT ID
    calls to booking function to process booking
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': 'User identity not found'}), 401

        data = request.json
        logger.info(f"Received booking request from feature for user {user_id}: {data}")

        result, status_code = booking_flight(data, user_id)
        logger.info(f"Booking result: {result}, Status code: {status_code}")
        return jsonify(result), status_code

    except Exception as e:
        logger.error(f"Error processing booking request: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
