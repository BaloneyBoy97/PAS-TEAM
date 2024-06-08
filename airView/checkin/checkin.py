
import logging
from flask import request, jsonify, make_response
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from authentication.operation import  get_booked_flights
import sqlite3


username = 'testuser'
get_booked_flights(username)
def fetch_booked_flights():
    data = request.get_json()
    username = data.get('username')
    if username:
        booked_flights = get_booked_flights(username)
        if booked_flights:
            return jsonify({'flights': booked_flights}), 200
        else:
            return jsonify({'message': 'No booked flights found for the user.'}), 404
    else:
        return jsonify({'message': 'Unauthorized access. Token invalid or expired.'}), 401
