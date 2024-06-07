#!/usr/bin/env python3
from flask import Blueprint, request, jsonify
from flask_mail import Mail
from flask_jwt_extended import get_jwt_identity
from booking.operation import booking_flight, get_available_seats

# create booking blueprint to define routes of booking page
booking_bp = Blueprint('booking_bp',__name__)

mail = Mail()

@booking_bp.route('/available_seats', methods=['GET'])
def available_seats():
    flight_id = request.args.get('flight_id')
    if not flight_id:
        return jsonify({'error': 'Null Input'}), 400
    seats = get_available_seats(flight_id)
    return jsonify(seats)

@booking_bp.route('/book', methods=['POST'])
def book():
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    data = request.json
    result = booking_flight(data, user_id, mail)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result)

