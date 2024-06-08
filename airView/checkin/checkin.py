import logging
from flask import request, jsonify, make_response
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from authentication.operation import get_flight_details, get_user_details, get_user_by_username,  get_booked_flights
import sqlite3

"""
Define the directory path where you want to create the database.
Create the database file in database directory.
"""
database_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
os.makedirs(database_dir, exist_ok=True)

db_path = os.path.join(database_dir, 'appdata.db')

conn = sqlite3.connect(db_path)
curr = conn.cursor()

@app.route('/checkin', methods=['POST'])
def check_in():
    data = request.get_json()
    username = data.get('username')
    print(username)
    print("ihfdsasiuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuhhhhhhhhhhhhhhhh")
    if username:
        user = get_user_by_username(username)
        if user:
            user_id = user['userid']
            curr.execute("UPDATE bookings SET is_checked_in = ? WHERE userid = ?", (1, user_id))
            conn.commit()
            flight_details = get_booked_flights(username)
            if flight_details:
                flight_id = flight_details['flightid']
                flight = get_flight_details(flight_id)
                user_details = get_user_details(user_id)
                return jsonify({'flight_details': flight, 'user_details': user_details}), 200
            else:
                return jsonify({'message': 'No booked flights found for the user.'}), 404
        else:
            return jsonify({'message': 'User not found.'}), 404
    else:
        return jsonify({'message': 'Invalid request.'}), 400
