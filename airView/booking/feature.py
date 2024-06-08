#!/usr/bin/env python3
from flask import Blueprint, request, jsonify
from flask_mail import Mail
from .operation import book_flight, get_available_seats

# create booking blueprint to define routes of booking page
booking_bp = Blueprint('booking_bp',__name__)

mail = Mail()

@booking_bp.route('/available_seats', methods=['GET'])
def available_seats():
    return

@booking_bp.route('/book', methods=['POST'])
def book():
    return

