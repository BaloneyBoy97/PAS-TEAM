#!/usr/bin/env python3
import sqlite3
import hashlib

conn = sqlite3.connect("Userdata.db")
curr = conn.cursor()

curr.execute("""
CREATE TABLE IF NOT EXISTS Userdata (
    userID INT PRIMARY KEY,
    userName VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
)
""")

test, tpass = "tester", hashlib.sha256("123456".encode()).hexdigest()
test2, tpass2 = "tester2", hashlib.sha256("234567".encode()).hexdigest()
test3, tpass3 = "tester3", hashlib.sha256("11123456".encode()).hexdigest()
test4, tpass4 = "tester4", hashlib.sha256("22123456".encode()).hexdigest()
# print(tpass)
curr.execute('INSERT INTO Userdata (userName, Password) VALUES (?, ?)', (test, tpass))
curr.execute('INSERT INTO Userdata (userName, Password) VALUES (?, ?)', (test2, tpass2))
curr.execute('INSERT INTO Userdata (userName, Password) VALUES (?, ?)', (test3, tpass3))
curr.execute('INSERT INTO Userdata (userName, Password) VALUES (?, ?)', (test4, tpass4))
conn.commit()