#!/usr/bin/env python3
import sqlite3
import random
import os


# Define the directory path where you want to create the database
database_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
os.makedirs(database_dir, exist_ok=True)

# Create the database file in the specified directory
db_path = os.path.join(database_dir, 'appdata.db')

#create a new db named appdata
conn = sqlite3.connect(db_path)
curr = conn.cursor()

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
    status TEXT NOT NULL
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

# Create seat class table (first class/economy plus/etc.) to store different seat classes
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
    ('AA100', 'St. Louis', 'Los Angeles', '2024-06-01 08:00:00', '2024-06-01 11:00:00', 'Scheduled'),
    ('BA200', 'St. Louis', 'New York', '2024-06-02 09:00:00', '2024-06-02 12:00:00', 'Scheduled'),
    ('CA300', 'St. Louis', 'San Francisco', '2024-06-03 10:00:00', '2024-06-03 13:00:00', 'Scheduled'),
    ('DA400', 'St. Louis', 'Sydney', '2024-06-04 11:00:00', '2024-06-04 14:00:00', 'Scheduled'),
    ('EA500', 'St. Louis', 'Tokyo', '2024-06-05 12:00:00', '2024-06-05 15:00:00', 'Scheduled'),
    ('FA600', 'St. Louis', 'Chicago', '2024-06-06 13:00:00', '2024-06-06 16:00:00', 'Scheduled'),
    ('GA700', 'St. Louis', 'San Francisco', '2024-06-07 14:00:00', '2024-06-07 17:00:00', 'Scheduled'),
    ('HA800', 'St. Louis', 'Vancouver', '2024-06-08 15:00:00', '2024-06-08 18:00:00', 'Scheduled'),
    ('IA900', 'St. Louis', 'London', '2024-06-09 16:00:00', '2024-06-09 19:00:00', 'Scheduled'),
    ('JA1000', 'St. Louis', 'Buenos Aires', '2024-06-10 17:00:00', '2024-06-10 20:00:00', 'Scheduled'),
    ('KA1100', 'St. Louis', 'Dubai', '2024-06-11 18:00:00', '2024-06-11 21:00:00', 'Scheduled'),
    ('LA1200', 'St. Louis', 'Cairo', '2024-06-12 19:00:00', '2024-06-12 22:00:00', 'Scheduled'),
    ('MA1300', 'St. Louis', 'Miami', '2024-06-13 20:00:00', '2024-06-13 23:00:00', 'Scheduled'),
    ('NA1400', 'St. Louis', 'Lisbon', '2024-06-14 21:00:00', '2024-06-15 00:00:00', 'Scheduled'),
    ('OA1500', 'St. Louis', 'Sydney', '2024-06-15 22:00:00', '2024-06-16 01:00:00', 'Scheduled')
]

# Insert sample data into flights table
curr.executemany("INSERT INTO flights (flightnumber, origin, destination, departuretime, arrivaltime, status) VALUES (?, ?, ?, ?, ?, ?)", flights)

# Create sample seat classes and insert it into seat class table
seat_class = [
    ('Economy',),
    ('Economy Plus',),
    ('Business',),
    ('First Class',)
]
curr.executemany("INSERT INTO seat_classes (classname) VALUES (?)", seat_class)

# create mock data for seat prices for each flights
seats = []
for flight_id in range(1, 16): # 15 mock flights data
    for class_id in range(1, 5): # 4 sample seats class
        for seat_number in range(1, 10): # assuming 10 seats in each class
            # create randomnized seats prices using random
            seat_id = len(seats) + 1
            seat_num = f'{class_id}-{seat_number}'
            price = random.uniform(79.99, 359.79) * class_id
            seats.append((seat_id, flight_id, seat_num, class_id, 1, price))
curr.executemany("INSERT INTO seats (seatid, flightid, seatnumber, classid, is_available, price) VALUES (?, ?, ?, ?, ?, ?)", seats)

# 
# Commit changes and close connection
conn.commit()
conn.close()
