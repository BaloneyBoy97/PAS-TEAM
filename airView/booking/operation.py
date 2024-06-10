#!/usr/bin/env python3
from flask_mail import Message
import sqlite3
import datetime
import os

def get_db_connection():
    DATABASE = os.path.join(os.path.dirname(__file__), '..', 'database', 'appdata.db')
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_available_seats(flight_id, class_id):
    return

def booking_flight(data, mail):
    return

