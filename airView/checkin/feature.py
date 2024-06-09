from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from checkin.operation import check_in_flight
from checkin.operation import get_booked_flights, get_flight_details

checkin_bp = Blueprint('checkin_bp', __name__)

@checkin_bp.route('/check-in', methods=['POST'])
@jwt_required()
def check_in():
    data = request.get_json()
    # email = data.get('email')
    # password = data.get('password')
    user_id = get_jwt_identity()
    data = request.json
    result, status_code = check_in_flight(data, user_id)
    return jsonify(result), status_code

@checkin_bp.route('/get-booked-flights', methods=['GET'])
@jwt_required()
def get_booked_flights_endpoint():
    try:
        username = get_jwt_identity()
        print(username)
        #username = "testuser"  # ---------------------------------hardcoded-------------
        if username:
            user_id, booked_flights = get_booked_flights(username)
            if booked_flights:
                flight_id = booked_flights['flightid']  # Assuming 'flightid' is the column name
                # Get flight details using the flight_id
                flight_details = get_flight_details(flight_id)
                # Extract data from the sqlite3.Row object
                # for column_name in flight_details.keys():
                #     print(f"{column_name}: {flight_details[column_name]}")
                flights_data = dict(flight_details)
                flights_data['user_id'] = user_id
                return jsonify({'flights': flights_data}), 200
            else:
                return jsonify({'message': 'No booked flights found for the user.'}), 404
        else:
            return jsonify({'message': 'Unauthorized access. Token invalid or expired.'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500