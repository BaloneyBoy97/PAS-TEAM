from flask import Blueprint, request, jsonify
from admin.operation import get_all_flights, create_flight, update_flight, delete_flight
import logging
admin_bp = Blueprint('admin_bp', __name__)

# Flight Management Routes
@admin_bp.route('/admin/api/flights', methods=['GET'])
def list_flights():
    try:
        flights = get_all_flights()
        return jsonify(flights), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/flights', methods=['POST'])
def add_flight():
    try:
        data = request.get_json()
        flightnumber = data.get('flightnumber')
        origin = data.get('origin')
        destination = data.get('destination')
        departuretime = data.get('departuretime')
        arrivaltime = data.get('arrivaltime')
        status = data.get('status')
        gate_number = data.get('gate_number')
        
        # Log the received payload data
        logging.info("Received request to create flight: %s", data)
        
        create_flight(flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number)
        
        return jsonify({'message': 'Flight created successfully'}), 201
    except Exception as e:
        logging.error('An error occurred while creating flight: %s', str(e))
        return jsonify({'error': 'Failed to create flight. Please check server logs for details.'}), 500

@admin_bp.route('/api/flights/<int:flight_id>', methods=['PUT'])
def edit_flight(flight_id):
    try:
        data = request.get_json()
        update_flight(flight_id, data['flightnumber'], data['origin'], data['destination'], data['departuretime'], data['arrivaltime'], data['status'], data['gate_number'])
        return jsonify({'message': 'Flight updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/flights/<int:flight_id>', methods=['DELETE'])
def remove_flight(flight_id):
    try:
        delete_flight(flight_id)
        return jsonify({'message': 'Flight deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
