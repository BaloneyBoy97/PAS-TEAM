from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
# from checkin.operation import check_in_flight
from checkin.operation import get_booked_flights, get_flight_details, check_in

checkin_bp = Blueprint('checkin_bp', __name__)

@checkin_bp.route('/get-booked-flights', methods=['GET'])
@jwt_required()
def get_booked_flights_endpoint():
    try:
        user_id = get_jwt_identity()
        if user_id:
            booked_flights = get_booked_flights(user_id)
            if booked_flights:
                flights_data = []
                for flight in booked_flights:
                    flight_id = flight[2]  # Assuming 'flightid' is the column name
                    is_checked_in = flight[7]
                    # Get flight details using the flight_id
                    flight_details = get_flight_details(flight_id)
                    if flight_details:
                        flight_detail_list = list(flight_details)
                        flight_detail_list.append(is_checked_in)
                        flights_data.append(flight_detail_list)
                # Extract data from the sqlite3.Row object
                # for column_name in flight_details.keys():
                #     print(f"{column_name}: {flight_details[column_name]}")
                flights_data.append(user_id)
                return jsonify({'flights': flights_data}), 200
            else:
                return jsonify({'message': 'No booked flights found for the user.'}), 404
        else:
            return jsonify({'message': 'Unauthorized access. Token invalid or expired.'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@checkin_bp.route('/check-in', methods=['POST'])
def handle_check_in():
    data = request.get_json()
    user_id = data.get('user_id')
    flight_id = data.get('flight_id')
    if not user_id:
        return jsonify({'message': 'User ID not provided'}), 400
    result = check_in(user_id,flight_id)
    return jsonify(result), 200 if result.get('message') == 'Check-in successful' else 500