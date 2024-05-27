#!/usr/bin/env python3
import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 1111))
server.listen()

def connection_handle(c):
    c.send("Username: ".encode())
    username = c.recv(1024).decode()
    c.send("Password: ".encode())
    password = c.recv(1024).decode()
    password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("Userdata.db")
    curr = conn.cursor()

    curr.execute("SELECT * FROM Userdata WHERE Username = ? AND Password = ?", (username, password))

    if curr.fetchall():
        c.send("Logged in!".encode())
    else:
        c.send("Failed!".encode())

while True:
    client, addr = server.accept()
    threading.Thread(target=connection_handle, args=(client,)).start()
