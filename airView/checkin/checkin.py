from flask import jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3

def check_in(user_id):
    try:
        database_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
        os.makedirs(database_dir, exist_ok=True)

        db_path = os.path.join(database_dir, 'appdata.db')

        conn = sqlite3.connect(db_path)
        curr = conn.cursor()

        if user_id:
            curr.execute("UPDATE bookings SET is_checked_in = ? WHERE userid = ?", (1, user_id))
            conn.commit()
            conn.close()  # Close the connection
            return jsonify({'message': 'Check-in successful'})
        else:
            conn.close()  # Close the connection
            return jsonify({'message': 'User ID not provided'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500