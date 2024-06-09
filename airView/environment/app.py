#!/usr/bin/env python3
import sys
import os
from flask import Flask, send_from_directory, jsonify, make_response, request, session
from flask_restful import Api
#from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from werkzeug.exceptions import HTTPException
from flask_mail import Mail
from dotenv import load_dotenv
from datetime import timedelta
import logging
import threading
import webbrowser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from authentication.operation import get_booked_flights, get_flight_details
from checkin.checkin import check_in

"""
Add parent directory to 
system path for modularization.
"""
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
import blueprints.
load environment.
initialize Flask.
"""
from authentication.feature import auth_bp
from booking.feature import booking_bp
from authentication import operation as auth_ops

load_dotenv()

app = Flask(__name__)

"""
Routes to Server:
    - Home Page
    - Sign Up Page
    - Forget Password Page
"""
@app.route('/')
def serve_html():
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'templates'), 'login.html')
    except Exception as e:
        app.logger.error('An error occurred while serving HTML: %s', str(e))
        return make_response(jsonify({'error': 'An internal server error occurred'}), 500)
    
@app.route('/home.html')
def login():
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'templates'), 'home.html')
    except Exception as e:
        app.logger.error('An error occurred while serving HTML: %s', str(e))
        return make_response(jsonify({'error': 'An internal server error occurred'}), 500)
    
@app.route('/check-in', methods=['POST'])
def handle_check_in():
    user_id = request.json.get('user_id')
    return check_in(user_id)

@app.route('/signup.html')
def signup():
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'templates'), 'signup.html')
    except Exception as e:
        app.logger.error('An error occurred while serving HTML: %s', str(e))
        return make_response(jsonify({'error': 'An internal server error occurred'}), 500)
    
@app.route('/forgot-password.html')
def forgetPassword():
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'templates'), 'forgot-password.html')
    except Exception as e:
        app.logger.error('An error occurred while serving HTML: %s', str(e))
        return make_response(jsonify({'error': 'An internal server error occurred'}), 500)

@app.route('/checkin.html')
def checkin():
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'templates'), 'checkin.html')
    except Exception as e:
        app.logger.error('An error occurred while serving HTML: %s', str(e))
        return make_response(jsonify({'error': 'An internal server error occurred'}), 500)
        
@app.route('/get-booked-flights', methods=['GET'])
#@jwt_required()
def get_booked_flights_endpoint():
    try:
        #username = get_jwt_identity()
        username = "testuser"  # ---------------------------------hardcoded-------------
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
    
# Configure app from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'supersecretjwtkey')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

"""
Set the database path from 
environment variables.
Initialize API, JWT, MAIL
"""
database_url = os.getenv('DATABASE_URL')
if database_url is None:
    database_url = os.path.join(os.path.dirname(__file__), '..', 'database', 'appdata.db')
app.config['DATABASE'] = database_url
auth_ops.set_database_path(app.config['DATABASE'])

api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)

"""
Logging and error handling
"""
logging.basicConfig(level=logging.DEBUG)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

@app.errorhandler(Exception)
def handle_exception(e):
    error_type = type(e).__name__
    app.logger.error('An error occurred: %s', str(e))
    app.logger.error('Error type: %s', error_type)
    
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = jsonify({'error': e.description}).data
        response.content_type = 'application/json'
        return response
    
    return make_response(jsonify({'error': 'An internal server error occurred'}), 500)

"""
Register Resource and blueprints
"""
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(booking_bp, url_prefix='/booking')

def open_browser():
    host = '127.0.0.1'
    port = 5000
    url = f"http://{host}:{port}/"
    webbrowser.open_new(url)

"""
Main entry point for the application
"""
if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threading.Timer(1, open_browser).start()
    
    app.run(debug=True)