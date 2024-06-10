from flask import Blueprint, request, jsonify
from flightsearch.operation import get_flights

flights_bp = Blueprint('flights', __name__)

@flights_bp.route('/search', methods=['GET'])
def search_flights():
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    departure_date = request.args.get('departure-date')
    
    if not all([departure, destination, departure_date]):
        return jsonify({'error': 'Missing required parameters'}), 400

    flights = get_flights(departure, destination, departure_date)
    return jsonify(flights)
