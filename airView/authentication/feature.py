#!/usr/bin/env python3
from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from email_validator import validate_email, EmailNotValidError
from authentication.operation import create_user, get_user_by_email, get_user_by_username, check_user_credentials
import logging

mail = Mail()  # Instantiate Mail object here
logger = logging.getLogger(__name__)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        # Input validation
        if not email or not username or not password:
            return jsonify({'message': 'Email, username, or password is empty!'}), 400

        # Email validation
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            return jsonify({'message': str(e)}), 400

        # Check if user already exists
        if get_user_by_email(email) or get_user_by_username(username):
            return jsonify({'message': 'User already exists!'}), 400
        
        # Create new user
        hashed_password = generate_password_hash(password)
        create_user(email, username, hashed_password)
        return jsonify({'message': 'User registered successfully!'}), 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Input validation
        if not email or not password:
            return jsonify({'message': 'Email or password is empty!'}), 400

        user = get_user_by_email(email)
        if user:
            logger.debug("User found during login attempt")
            logger.debug("Hashed password retrieved from database: %s", user['password'])
            if check_password_hash(user['password'], password):
                logger.debug("Password matched")
                return jsonify({'message': 'Logged in!'}), 200
            else:
                logger.debug("Invalid password")
        else:
            logger.debug("User not found during login attempt")

        logger.error("Login failed")
        return jsonify({'message': 'Failed!'}), 401


class AdminRegistration(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        # Input validation
        if not email or not username or not password:
            return jsonify({'message': 'Email, username, or password is empty!'}), 400

        # Email validation
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            return jsonify({'message': str(e)}), 400

        # Check if user already exists
        if get_user_by_email(email) or get_user_by_username(username):
            return jsonify({'message': 'User already exists!'}), 400

        # Create new admin user
        hashed_password = generate_password_hash(password)
        create_user(email, username, hashed_password, is_admin=True)
        return jsonify({'message': 'Admin registered successfully!'}), 201
