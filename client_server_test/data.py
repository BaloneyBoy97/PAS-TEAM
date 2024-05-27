#!/usr/bin/env python3
import sqlite3
import hashlib

conn = sqlite3.connect("appdata.db")
curr = conn.cursor()

curr.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

# Sample users with hashed passwords
test_users = [
    ("tester", hashlib.sha256("123456".encode()).hexdigest()),
    ("tester2", hashlib.sha256("234567".encode()).hexdigest()),
    ("tester3", hashlib.sha256("11123456".encode()).hexdigest()),
    ("tester4", hashlib.sha256("22123456".encode()).hexdigest())
]

for username, password in test_users:
    curr.execute('INSERT INTO userdata (username, password) VALUES (?, ?)', (username, password))

conn.commit()
conn.close()