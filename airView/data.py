#!/usr/bin/env python3
import sqlite3

#create a new db named appdata
conn = sqlite3.connect("appdata.db")
curr = conn.cursor()

# create user data table to store user information
curr.execute ("""
CREATE TABLE IF NOT EXISTS userdata(
    userid INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    isAdmin BOOLEAN NOT NULL DEFAULT 0
)
""")
# create flights table to store flight information
curr.execute ("""
CREATE TABLE IF NOT EXISTS flights(
    flightid INTEGER PRIMARY KEY,
    flightnumber TEXT UNIQUE NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    departuretime NOT NULL,
    arrivaltime TEXT NOT NULL,
    status TEXT NOT NULL
)
""")
# create bookings table to store user booking data
curr.execute ("""
CREATE TABLE IF NOT EXISTS bookings(
    bookingid INTEGER PRIMARY KEY,
    userid INTEGER,
    flightid INTEGER,
    FOREIGN KEY (userid) REFERENCES userdata(userid),
    FOREIGN KEY (flightid) REFERENCES flights(flightid)
)
""")

conn.commit()
conn.close()