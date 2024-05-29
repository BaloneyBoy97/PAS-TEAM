#!/usr/bin/env python3
import sqlite3

# perform user registration and add user data to db
def create_user(email, username, password, is_admin=False):
    conn = sqlite3.connect("appdata.db")
    curr = conn.cursor()
    curr.execute("INSERT INTO userdata (email, userName, Password, is_admin) VALUES (?, ?, ?, ?)",
                 (email, username, password, is_admin))
    conn.commit()
    conn.close()

# check user email existance
def get_user_by_email(email):
    conn = sqlite3.connect("appdata.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM userdata WHERE email = ?", (email,))
    user = curr.fetchone()
    conn.close()
    return user
# check username existance
def get_user_by_username(username):
    conn = sqlite3.connect("appdata.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM userdata WHERE username = ?", (username,))
    user = curr.fetchone()
    conn.close()
    if user:
        return {'email': user[0], 'username': user[1], 'password': user[2], 'is_admin': user[3]}
    return None

# if user email and password match, then log in user
def check_user_credentials(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user[3], password): 
        return True
    return False