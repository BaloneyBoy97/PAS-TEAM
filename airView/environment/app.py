#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, send_from_directory, jsonify, make_response, request, redirect, url_for
from flask_restful import Api
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
# from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
from datetime import timedelta
import logging
from authentication.feature import UserRegistration, UserLogin, AdminRegistration, UserLogout

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Connect to HTML homepage
@app.route('/')
def serve_html():
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'templates'), 'login.html')
    except Exception as e:
        app.logger.error('An error occurred while serving HTML: %s', str(e))
        return make_response(jsonify({'error': 'An internal server error occurred'}), 500)
    
@app.route('/home')
def home():
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'templates'), 'home.html')
    except Exception as e:
        app.logger.error('An error occurred while serving HTML: %s', str(e))
        return make_response(jsonify({'error': 'An internal server error occurred'}), 500)

@app.route('/admin-home')
def admin_home():
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'templates'), 'admin-home.html')
    except Exception as e:
        app.logger.error('An error occurred while serving HTML: %s', str(e))
        return make_response(jsonify({'error': 'An internal server error occurred'}), 500)

@app.route('/signup')
def signup():
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'templates'), 'signup.html')
    except Exception as e:
        app.logger.error('An error occurred while serving HTML: %s', str(e))
        return make_response(jsonify({'error': 'An internal server error occurred'}), 500)
    
@app.route('/forgot-password')
def forget_password():
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'templates'), 'forgot-password.html')
    except Exception as e:
        app.logger.error('An error occurred while serving HTML: %s', str(e))
        return make_response(jsonify({'error': 'An internal server error occurred'}), 500)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = UserLogin().post()
    response_data = response.get_json()
    
    if response.status_code == 200:
        if response_data.get('isAdmin'):
            return redirect(url_for('admin_home'))
        else:
            return redirect(url_for('home'))
    return response

# Configure app from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Initialize extensions
api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
