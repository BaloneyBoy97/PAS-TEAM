#!/usr/bin/env python3
from flask import request, jsonify, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from flask_mail import Mail, Message
from email_validator import validate_email, EmailNotValidError
from authentication.operation import create_user, get_user_by_email, get_user_by_username, check_user_credentials
import logging
import sqlite3

# Initialize mail
mail = Mail()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not email or not username or not password:
            logger.warning('Empty email, username, or password in registration attempt.')
            return make_response(jsonify({'message': 'Email, username, or password is empty!'}), 400)

        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            logger.error('Email validation error: %s', str(e))
            return make_response(jsonify({'message': str(e)}), 400)

        if get_user_by_email(email) or get_user_by_username(username):
            logger.warning('Registration attempt with existing email or username: %s, %s', email, username)
            return make_response(jsonify({'message': 'User already exists!'}), 400)
        
        hashed_password = generate_password_hash(password)
        create_user(email, username, hashed_password)
        logger.info('User registered successfully: %s', email)
        return make_response(jsonify({'message': 'User registered successfully!'}), 201)

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            logger.warning('Login attempt with empty email or password')
            return make_response(jsonify({'error': 'Email or password is empty!'}), 400)

        logger.debug('Attempting to log in user with email: %s', email)
        user = get_user_by_email(email)
        if user:
            logger.debug('User found with email: %s', email)
            if check_user_credentials(password, email):
                logger.info('User logged in successfully: %s', email)
                access_token = create_access_token(identity=email)
                return make_response(jsonify({'message': 'Logged in!', 'access_token': access_token, 'username': user['username']}), 200)
            else:
                logger.warning('Invalid password attempt for email: %s', email)
        else:
            logger.warning('No user found with email: %s', email)
        
        return make_response(jsonify({'error': 'Invalid email or password!'}), 401)

class AdminRegistration(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not email or not username or not password:
            logger.warning('Empty email, username, or password in admin registration attempt.')
            return make_response(jsonify({'message': 'Email, username, or password is empty!'}), 400)

        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            logger.error('Email validation error: %s', str(e))
            return make_response(jsonify({'message': str(e)}), 400)

        if get_user_by_email(email) or get_user_by_username(username):
            logger.warning('Admin registration attempt with existing email or username: %s, %s', email, username)
            return make_response(jsonify({'message': 'User already exists!'}), 400)

        hashed_password = generate_password_hash(password)
        create_user(email, username, hashed_password, is_admin=True)
        logger.info('Admin registered successfully: %s', email)
        return make_response(jsonify({'message': 'Admin registered successfully!'}), 201)

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        response = jsonify({'message': 'Logged out successfully!'})
        unset_jwt_cookies(response)
        logger.info('User logged out: %s', email)
        response.status_code = 200
        return response

class UserBookedFlights(Resource):
    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        try:
            user = get_user_by_email(email)
            if user:
                user_id = user['userid']
                flights = get_booked_flights(user_id)
                return make_response(jsonify({'flights': flights}), 200)
            else:
                return make_response(jsonify({'error': 'User not found'}), 404)
        except Exception as e:
            logger.error('Error fetching booked flights: %s', e)
            return make_response(jsonify({'error': 'An error occurred while fetching booked flights'}), 500)

def get_booked_flights(user_id):
    try:
        with get_db_connection() as conn:
            flights = conn.execute('''
                SELECT f.flightnumber, f.origin, f.destination, f.departuretime, f.arrivaltime, f.status, f.gate_number
                FROM bookings b
                JOIN flights f ON b.flightid = f.flightid
                WHERE b.userid = ?
            ''', (user_id,)).fetchall()
        return [dict(flight) for flight in flights]
    except sqlite3.Error as e:
        logger.error('Error retrieving booked flights: %s', e)
        return []

def get_db_connection():
    # This function should return a database connection
    # Replace with your actual database connection code
    pass
