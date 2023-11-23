import tkinter as tk
import socket
import threading
# import sys

class Client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8080
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.host, self.port))
        
    def broadcast(self, text_area):
        try:
            while True:
                receivedMessage = self.clientSocket.recv(1024).decode()
                if(receivedMessage != "PING"):
                    text_area.insert(tk.END, "\n" + receivedMessage)
                else:
                    returnPingMessage = "PONG"
                    try:
                        self.clientSocket.send(returnPingMessage.encode())
                    except ConnectionError:
                        raise ConnectionError("Server is closed or unavailable")
        except ConnectionError as err:
            raise ConnectionError("Server is closed or unavailable")
            # sys.__excepthook__(type(err), err, err.__traceback__)
    def sendCommand(self, command):
        try:
            self.clientSocket.send(command.encode())
        except ConnectionError:
            raise ConnectionError("Server is closed or unavailable")
        
    def run(self, text_area):
        receiveThread = threading.Thread(target = self.broadcast, args= (text_area, ))
        receiveThread.start()