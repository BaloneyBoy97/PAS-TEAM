#!/usr/bin/env python3
from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from flask_mail import Mail, Message
from email_validator import validate_email, EmailNotValidError
from authentication.operation import create_user, get_user_by_email, get_user_by_username, check_user_credentials
import logging

"""
Initialize Mail instance.
Logging set up.
"""
mail = Mail()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

"""
User Authentication Blueprint
"""
auth_bp = Blueprint('auth_bp', __name__)
api = Api(auth_bp)

class UserRegistration(Resource):
    """
    Checking for empty field when registering.
    Validate email, and check for existing user.
    Create new user if all check pass
    """
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
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        create_user(email, username, hashed_password)
        logger.info('User registered successfully: %s', email)

        self.registration_notification(email, username)

        return make_response(jsonify({'message': 'User registered successfully!'}), 201)
    
    def registration_notification(self, email, username):  # Corrected method name
        msg = Message('Welcome to Our AirView!', recipients=[email])
        msg.body = f"""
        Hi {username},

        Thank you for registering with AirView!

        Best regards,
        The PSD AirView Team
        """
        mail.send(msg)


class UserLogin(Resource):
    """
    Checking for empty field when login.
    fetch user's email and authenticate
    user credentials before login.
    """
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
                access_token = create_access_token(identity=user['userid'])
                return make_response(jsonify({'message': 'Logged in!', 'access_token': access_token, 'username': user['username']}), 200)
            else:
                logger.warning('Invalid password attempt for email: %s', email)
        else:
            logger.warning('No user found with email: %s', email)
        
        return make_response(jsonify({'error': 'Invalid email or password!'}), 401)

class AdminRegistration(Resource):
    """
    same logic as user login
    """
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
    """
    fetch user email and unset JWT cookies
    """
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        response = jsonify({'message': 'Logged out successfully!'})
        unset_jwt_cookies(response)
        logger.info('User logged out: %s', email)
        response.status_code = 200
        return response
"""
register the resource routes with blueprint
"""
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(AdminRegistration, '/admin/register')