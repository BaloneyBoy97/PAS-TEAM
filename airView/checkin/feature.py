# checkin/feature.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from checkin.operation import get_booked_flights, get_flight_details, check_in
import logging

checkin_bp = Blueprint('checkin_bp', __name__)
logger = logging.getLogger(__name__)

@checkin_bp.route('/get-booked-flights', methods=['GET'])
@jwt_required()
def get_booked_flights_endpoint():
    try:
        user_id = get_jwt_identity()
        logger.debug(f"User ID: {user_id}")
        if user_id:
            booked_flights = get_booked_flights(user_id)
            logger.debug(f"Booked Flights: {booked_flights}")
            if booked_flights:
                flights_data = []
                for flight in booked_flights:
                    flight_id = flight[2]  # Assuming 'flightid' is the column name
                    is_checked_in = flight[7]
                    # Get flight details using the flight_id
                    flight_details = get_flight_details(flight_id)
                    logger.debug(f"Flight Details for Flight ID {flight_id}: {flight_details}")
                    if flight_details:
                        flight_detail_list = list(flight_details)
                        flight_detail_list.append(is_checked_in)
                        flights_data.append(flight_detail_list)
                flights_data.append(user_id)
                logger.debug(f"Final Flights Data: {flights_data}")
                return jsonify({'flights': flights_data}), 200
            else:
                logger.debug("No booked flights found for the user.")
                return jsonify({'message': 'No booked flights found for the user.'}), 404
        else:
            logger.debug("Unauthorized access. Token invalid or expired.")
            return jsonify({'message': 'Unauthorized access. Token invalid or expired.'}), 401
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@checkin_bp.route('/check-in', methods=['POST'])
@jwt_required()
def handle_check_in():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        flight_id = data.get('flight_id')
        if not user_id:
            return jsonify({'message': 'User ID not provided'}), 400
        if not flight_id:
            return jsonify({'message': 'Flight ID not provided'}), 400
        result, status_code = check_in(user_id, flight_id)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500