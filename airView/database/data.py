#!/usr/bin/env python3
import sqlite3

# Create a new db named appdata
conn = sqlite3.connect("appdata.db")
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
    FOREIGN KEY (userid) REFERENCES userdata(userid),
    FOREIGN KEY (flightid) REFERENCES flights(flightid)
)
""")

# Sample data for userdata table
sample_userdata = [
    ('john.doe@example.com', 'JohnDoe', 'password123', 0),
    ('jane.smith@example.com', 'JaneSmith', 'pass456', 0),
    ('admin@example.com', 'Admin', 'adminpass', 1),
    ('mike.jones@example.com', 'MikeJones', 'mike789', 0),
    ('alice.brown@example.com', 'AliceBrown', 'alice987', 0),
    ('charlie.davis@example.com', 'CharlieDavis', 'charlie654', 0),
    ('david.evans@example.com', 'DavidEvans', 'david321', 0),
    ('eve.foster@example.com', 'EveFoster', 'eve111', 0),
    ('frank.green@example.com', 'FrankGreen', 'frank222', 0),
    ('grace.harris@example.com', 'GraceHarris', 'grace333', 0),
    ('henry.ingham@example.com', 'HenryIngham', 'henry444', 0),
    ('ivy.johnson@example.com', 'IvyJohnson', 'ivy555', 0),
    ('jack.king@example.com', 'JackKing', 'jack666', 0),
    ('kate.lee@example.com', 'KateLee', 'kate777', 0),
    ('leo.martin@example.com', 'LeoMartin', 'leo888', 0)
]

# Insert sample data into userdata table
curr.executemany("INSERT INTO userdata (email, username, password, isAdmin) VALUES (?, ?, ?, ?)", sample_userdata)

# Commit changes and close connection
conn.commit()
conn.close()
