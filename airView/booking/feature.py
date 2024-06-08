from flask import Blueprint, request, jsonify
from flask_mail import Mail
from flask_jwt_extended import jwt_required, get_jwt_identity
from booking.operation import booking_flight, get_available_seats, set_mail_instance

# create booking blueprint to define routes of booking page
booking_bp = Blueprint('booking_bp', __name__)

# Initialize Mail object for Email Notification
mail = Mail()

# send mail instance to booking/operation.py for Email operation
set_mail_instance(mail)

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
    seats = get_available_seats(flight_id)
    return jsonify(seats)

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
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    data = request.json
    result, status_code = booking_flight(data, user_id)
    return jsonify(result), status_code