#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime

# Define the directory path where you want to create the database
database_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
os.makedirs(database_dir, exist_ok=True)

# Create the database file in the specified directory
db_path = os.path.join(database_dir, 'appdata.db')

def create_tables_and_insert_data(db_path):
    with sqlite3.connect(db_path) as conn:
        curr = conn.cursor()
        
        # Enable foreign key support
        curr.execute("PRAGMA foreign_keys = ON")
        
        # Create user data table to store user information
        curr.execute("""
        CREATE TABLE IF NOT EXISTS userdata(
            userid INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            isAdmin BOOLEAN NOT NULL DEFAULT 0
        )
        """)
        
        # Create flights table to store flight information
        curr.execute("""
        CREATE TABLE IF NOT EXISTS flights(
            flightid INTEGER PRIMARY KEY,
            flightnumber TEXT UNIQUE NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            departuretime TEXT NOT NULL,
            arrivaltime TEXT NOT NULL,
            status TEXT NOT NULL,
            gate_number TEXT NOT NULL
        )
        """)
        
        # Create bookings table to store user booking data
        curr.execute("""
            CREATE TABLE IF NOT EXISTS bookings(
                bookingid INTEGER PRIMARY KEY,
                userid INTEGER,
                flightid INTEGER,
                classid INTEGER,
                seatid INTEGER,
                num_luggage INTEGER,
                booking_time TEXT NOT NULL,
                FOREIGN KEY (userid) REFERENCES userdata(userid),
                FOREIGN KEY (flightid) REFERENCES flights(flightid),
                FOREIGN KEY (classid) REFERENCES seat_classes(classid),
                FOREIGN KEY (seatid) REFERENCES seats(seatid)
            )
        """)
        
        # Create seat class table to store different seat classes
        curr.execute("""
            CREATE TABLE IF NOT EXISTS seat_classes(
                classid INTEGER PRIMARY KEY,
                classname TEXT NOT NULL
            )
        """)
        
        # Create seats table to store seating information in a flight
        curr.execute("""
            CREATE TABLE IF NOT EXISTS seats(
                seatid INTEGER PRIMARY KEY,
                flightid INTEGER,
                seatnumber TEXT NOT NULL,
                classid INTEGER,
                price REAL,
                is_available BOOLEAN NOT NULL DEFAULT 1,
                FOREIGN KEY (flightid) REFERENCES flights(flightid),
                FOREIGN KEY (classid) REFERENCES seat_classes(classid)
            )
        """)
        
        # Create luggage table to store luggage information
        curr.execute("""
            CREATE TABLE IF NOT EXISTS luggage(
                luggageid INTEGER PRIMARY KEY,
                bookingid INTEGER,
                weight REAL NOT NULL,
                free_luggage INTEGER DEFAULT 0,
                paid_luggage INTEGER DEFAULT 0,
                FOREIGN KEY (bookingid) REFERENCES bookings(bookingid)
            )
        """)
        
        # Sample data for flights table
        flights = [
            ('AA100', 'St. Louis', 'Los Angeles', '2024-06-01 08:00:00', '2024-06-01 11:00:00', 'Scheduled', "Gate A1"),
            ('BA200', 'St. Louis', 'New York', '2024-06-02 09:00:00', '2024-06-02 12:00:00', 'Scheduled', "Gate B2"),
        ]
        
        # Insert sample data into flights table
        curr.executemany("INSERT INTO flights (flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number) VALUES (?, ?, ?, ?, ?, ?, ?)", flights)
        
        # Create sample seat classes and insert into seat class table
        seat_classes = [
            ('Economy',),
            ('Economy Plus',),
            ('Business',),
            ('First Class',)
        ]
        curr.executemany("INSERT INTO seat_classes (classname) VALUES (?)", seat_classes)
        
        
        # Hardcoded mock data for bookings
        bookings = [
            (1, 1, 1, 1, 1, '2024-06-01 07:00:00'),
            (2, 2, 2, 11, 2, '2024-06-02 08:00:00')
        ]
        
        curr.executemany("INSERT INTO bookings (userid, flightid, classid, seatid, num_luggage, booking_time) VALUES (?, ?, ?, ?, ?, ?)", bookings)
        
        # Commit changes (auto-committed with the context manager)
    print("Database tables created and sample data inserted successfully.")

if __name__ == "__main__":
    create_tables_and_insert_data(db_path)
