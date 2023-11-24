import tkinter as tk
import socket
import threading
import sys
# library for FTP server
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftplib import FTP
import os

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
                if(receivedMessage == "PING"):
                    returnPingMessage = "PONG"
                    try:
                        self.clientSocket.send(returnPingMessage.encode())
                    except ConnectionError:
                        raise ConnectionError("Server is closed or unavailable")
                elif(receivedMessage.split(' ')[0] == "fetching"):
                    portname = receivedMessage.split(' ')[2]
                    filename = receivedMessage.split(' ')[1]
                    print("receive fetching command {} {}".format(portname, filename))
                    peer_client = ClientFTPClient()
                    peer_client.connect('127.0.0.1', int(portname), 'user', '12345')
                    # print("Remote path: ", "./{}/{}".format(portname, filename))
                    # print("Local path: ", "./{}".format(sys.argv[1]))
                    peer_client.download_file("./{}/{}".format(portname, filename), "./{}".format(sys.argv[1]))
                    # peer_client.download_file('./21/vid.mp4', './22')
                else:
                    text_area.insert(tk.END, "\n" + receivedMessage)
                    
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
        
class ClientFTPServer:
    def __init__(self, address, username, password, directory):
        self.address = address
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_user(username, password, directory, perm='elradfmwMT')
        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer
        self.server = FTPServer(self.address, self.handler)

    def start_server(self):
        self.server.serve_forever()
        
class ClientFTPClient:
    def __init__(self):
        self.ftp = FTP()

    def connect(self, host, port, username, password):
        self.ftp.connect(host, port)
        self.ftp.login(username, password)

    def upload_file(self, local_file_path, remote_file_path):
        with open(local_file_path, 'rb') as file:
            self.ftp.storbinary(f"STOR {remote_file_path}", file)

    def download_file(self, remote_file_path, local_folder_path):
        try:
            filename = os.path.basename(remote_file_path)  # Extract filename from remote path
            local_file_path = os.path.join(local_folder_path, "copy_" + filename)
            with open(local_file_path, 'wb') as file:
                self.ftp.retrbinary(f"RETR {remote_file_path}", file.write)
            print(f"File downloaded to '{local_file_path}' successfully.")
        except Exception as e:
            print(f"Error downloading file: {e}")