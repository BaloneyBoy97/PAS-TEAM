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
        is_checkedin BOOLEAN NOT NULL DEFAULT 0,
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

# create unique rng gate number
gates = [f"Gate {letter}{number}" for letter in 'ABCDE' for number in range(1, 31)]
random.shuffle(gates)

# Sample data for flights table
flights = [
    ('AA100', 'St. Louis', 'Los Angeles', '2024-06-01 08:00:00', '2024-06-01 11:00:00', 'Scheduled', gates.pop()),
    ('BA200', 'St. Louis', 'New York', '2024-06-02 09:00:00', '2024-06-02 12:00:00', 'Scheduled', gates.pop()),
    ('CA300', 'St. Louis', 'San Francisco', '2024-06-03 10:00:00', '2024-06-03 13:00:00', 'Scheduled', gates.pop()),
    ('DA400', 'St. Louis', 'Sydney', '2024-06-04 11:00:00', '2024-06-04 14:00:00', 'Scheduled', gates.pop()),
    ('EA500', 'St. Louis', 'Tokyo', '2024-06-05 12:00:00', '2024-06-05 15:00:00', 'Scheduled', gates.pop()),
    ('FA600', 'St. Louis', 'Chicago', '2024-06-06 13:00:00', '2024-06-06 16:00:00', 'Scheduled', gates.pop()),
    ('GA700', 'St. Louis', 'San Francisco', '2024-06-07 14:00:00', '2024-06-07 17:00:00', 'Scheduled', gates.pop()),
    ('HA800', 'St. Louis', 'Vancouver', '2024-06-08 15:00:00', '2024-06-08 18:00:00', 'Scheduled', gates.pop()),
    ('IA900', 'St. Louis', 'London', '2024-06-09 16:00:00', '2024-06-09 19:00:00', 'Scheduled', gates.pop()),
    ('JA1000', 'St. Louis', 'Buenos Aires', '2024-06-10 17:00:00', '2024-06-10 20:00:00', 'Scheduled', gates.pop()),
    ('KA1100', 'St. Louis', 'Dubai', '2024-06-11 18:00:00', '2024-06-11 21:00:00', 'Scheduled', gates.pop()),
    ('LA1200', 'St. Louis', 'Cairo', '2024-06-12 19:00:00', '2024-06-12 22:00:00', 'Scheduled', gates.pop()),
    ('MA1300', 'St. Louis', 'Miami', '2024-06-13 20:00:00', '2024-06-13 23:00:00', 'Scheduled', gates.pop()),
    ('NA1400', 'St. Louis', 'Lisbon', '2024-06-14 21:00:00', '2024-06-15 00:00:00', 'Scheduled', gates.pop()),
    ('OA1500', 'St. Louis', 'Sydney', '2024-06-15 22:00:00', '2024-06-16 01:00:00', 'Scheduled', gates.pop())
]

# Insert sample data into flights table
curr.executemany("INSERT INTO flights (flightnumber, origin, destination, departuretime, arrivaltime, status, gate_number) VALUES (?, ?, ?, ?, ?, ?, ?)", flights)

# Create sample seat classes and insert it into seat class table
seat_class = [
    ('Economy',),
    ('Economy Plus',),
    ('Business',),
    ('First Class',)
]
curr.executemany("INSERT INTO seat_classes (classname) VALUES (?)", seat_class)

# create mock data for seat prices for each flights
# assign seat numbers (seperate from seat id exmp: 1A, 1B, 1C) similar to a boeing 737
seats = []
columns = 'ABCDEF' # 6 seats per row
rows_per_class = {
    'First Class': 6,
    'Business': 6,
    'Economy Plus': 10,
    'Economy': 24
} # 6 rows of first class, 6 rows of business class, 10 rows of economy plus and 24 rows of economy

# generate a price range for each class
price_ranges = {
    'First Class': (300.00, 400.00),
    'Business': (200.00, 300.00),
    'Economy Plus': (100.00, 200.00),
    'Economy': (50.00, 100.00)
}

classNames = ['First Class', 'Business', 'Economy Plus', 'Economy']
class_id_map = {name: idx + 1 for idx, name in enumerate(classNames)} # mapping seat class names to seat id

for flight_id in range(1, 16):  # flights data (created 15 mock data)
    current_row = 1
    for name in classNames: # assign seat class id
        class_id = class_id_map[name]
        num_rows = rows_per_class[name] # pull number of rows for the loop to generate seat number and price
        min_price, max_price = price_ranges[name]
        for row in range(current_row, current_row + num_rows): # 1-6, 7-12, 13-23, 24-48
            for column in columns: # A-F
                seat_id = len(seats) + 1 # auto increment generated id
                seat_num = f'{row}{column}' #1A,1B,1C, etc
                price = round(random.uniform(min_price, max_price), 2)
                seats.append((seat_id, flight_id, seat_num, class_id, price, 1))
        current_row += num_rows
curr.executemany("INSERT INTO seats (seatid, flightid, seatnumber, classid, price, is_available) VALUES (?, ?, ?, ?, ?, ?)", seats)

# Commit changes and close connection
conn.commit()
conn.close()