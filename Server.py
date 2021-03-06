import time
import socket
import json
import os
import sys
from platform import system

os.chdir(os.path.dirname(sys.argv[0]))
with open("config.json", "r") as f:
    data = json.load(f)

    DEFAULTPORT = data["defaultport"]
    PORT = DEFAULTPORT
    ignoreQuotation = data["server"]["ignoreQuotation"]
    VERSION = data ["server"]["version"]

class Server:
    def __init__(self):
        self.s = socket.socket()
    
        print("PySH Server")
        print("Version: {}".format(VERSION))
        print("-"*25)
        
    def get_info(self):
        # self.HOST = str(input("Please enter the IP address of the device you want to connect to: "))
        self.PORT = input("Please enter the Port to use for connecting. (leave empty to use default port: {}): ".format(DEFAULTPORT))

        if self.PORT == "":
            self.PORT = PORT
            return

        try:
            self.PORT = int(self.PORT)
        except ValueError:
            print("Port must be an Integer!")

    def establish_connection(self, PORT):
        global conn

        if system() != "Darwin":
            self.host = socket.gethostname()
        else:
            self.host = "localhost"
        
        self.s.bind(("", PORT))
        print("Server is ready.")
        print("Connection Address: {}:{}".format(socket.gethostbyname(self.host), self.PORT))
        print("Waiting for Client...")
        self.s.listen()
        
        self.conn, self.addr = self.s.accept()
        print("{} connected.".format(self.addr))

    def send_command(self):
        global conn
        
        self.command = input(str("Command: "))

        if self.command == "":
            print("Can't send Empty Message!")
            return

        if ignoreQuotation == True:
            self.command = self.command.replace("'", "\\'")
        
        self.conn.send(self.command.encode())

        print("Sent command to Client.")
        self.data = self.conn.recv(1024)

        if self.data:
            print("Client received command.")
        else:
            return

def run_server():
    serv = Server()
    
    serv.get_info()
    serv.establish_connection(PORT)
    while True:
        serv.send_command()

if __name__ == "__main__":
    run_server()
