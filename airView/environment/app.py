#!/usr/bin/env python3
import sys
import os
import webbrowser
import threading
from flask import Flask, send_from_directory, jsonify, make_response
from flask_restful import Api
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
# from flask_cors import CORS  # Uncomment if CORS is needed
from flask_mail import Mail
from dotenv import load_dotenv
from datetime import timedelta
import logging
import threading
import webbrowser

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from authentication.feature import UserRegistration, UserLogin, AdminRegistration, UserLogout, UserBookedFlights

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Uncomment if CORS is needed
# CORS(app)

# connect to HTML homepage

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

    
# Configure app from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'supersecretjwtkey')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'localhost')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 25))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'False').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Initialize extensions
api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)

# Logging configuration
logging.basicConfig(level=logging.DEBUG)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

# Add a global error handler to catch any unhandled exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    error_type = type(e).__name__
    app.logger.error('An error occurred: %s', str(e))
    app.logger.error('Error type: %s', error_type)
    
    # Handle HTTPException specifically
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = jsonify({'error': e.description}).data
        response.content_type = 'application/json'
        return response
    
    # Handle generic exceptions
    return make_response(jsonify({'error': 'An internal server error occurred'}), 500)

# Add resource endpoints
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(AdminRegistration, '/admin/register')
api.add_resource(UserBookedFlights, '/api/booked-flights')

def open_browser():
    host = '127.0.0.1'
    port = 5000
    url = f"http://{host}:{port}/"
    webbrowser.open_new(url)

# Run the app
if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threading.Timer(1, open_browser).start()  # Open browser after 1 second delay
    
    app.run(debug=True)
