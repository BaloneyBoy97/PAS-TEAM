from flask import request, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from authentication.operation import get_flight_details, get_user_details, get_user_by_username,  get_booked_flights
import sqlite3
from database.data import curr, conn

def check_in(user_id):
    if user_id:
        curr.execute("UPDATE bookings SET is_checked_in = ? WHERE userid = ?", (1, user_id))
        conn.commit()
    else:
        return jsonify({'message': '.'}), 404
