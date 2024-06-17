from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from admin.operation import get_all_flights, create_flight, update_flight, delete_flight

admin_bp = Blueprint('admin_bp', __name__)

# Flight Management Routes
@admin_bp.route('/api/flights', methods=['GET'])
def list_flights():
    flights = get_all_flights()
    return jsonify(flights)

@admin_bp.route('/api/flights', methods=['POST'])
def add_flight():
    data = request.get_json()
    create_flight(data['flightnumber'], data['origin'], data['destination'], data['departuretime'], data['arrivaltime'], data['status'], data['gate_number'])
    return jsonify({'message': 'Flight created successfully'}), 201

@admin_bp.route('/api/flights/<int:flight_id>', methods=['PUT'])
def edit_flight(flight_id):
    data = request.get_json()
    update_flight(flight_id, data['flightnumber'], data['origin'], data['destination'], data['departuretime'], data['arrivaltime'], data['status'], data['gate_number'])
    return jsonify({'message': 'Flight updated successfully'})

@admin_bp.route('/api/flights/<int:flight_id>', methods=['DELETE'])
def remove_flight(flight_id):
    delete_flight(flight_id)
    return jsonify({'message': 'Flight deleted successfully'})
