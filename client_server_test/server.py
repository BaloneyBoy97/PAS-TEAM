#!/usr/bin/env python3
import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

def connection_handle(c):
    try:
        c.send("Username: ".encode())
        username = c.recv(1024).decode()
        c.send("Password: ".encode())
        password = c.recv(1024).decode()
        password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("appdata.db")
        curr = conn.cursor()

        curr.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

        if curr.fetchone():
            c.send("Logged in!".encode())
        else:
            c.send("Failed!".encode())

    except Exception as e:
        print(f"Error: {e}")
        c.send("Failed!".encode())
    finally:
        c.close()
        conn.close()

while True:
    client, addr = server.accept()
    threading.Thread(target=connection_handle, args=(client,)).start()
