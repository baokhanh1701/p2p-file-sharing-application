from .lib import *



class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.runningBroadcast = True # signal for broadcast function
        try:
            self.clientSocket.connect((self.host, self.port))
        except ConnectionRefusedError:
            raise ConnectionError("Can not connect to server")
        
        
    def broadcast(self, text_area):
        # global runningBroadcast
        try:
            while self.runningBroadcast:
                # print(self.runningBroadcast)
                try:
                    receivedMessage = json.loads(self.clientSocket.recv(1024).decode('utf-8'))
                    header = receivedMessage.get("HEADER")
                    payload = receivedMessage.get("PAYLOAD")
                    # check for ping message
                    if(header == "ping"):
                        time.sleep(0.1)
                        JSONpingMessage = convertJSONProtocol("message>client>pong")
                        self.clientSocket.sendall((JSONpingMessage).encode('utf-8'))
                        print("send pong to server")
                    else:
                        addTextToOutput(text_area, payload.get("message"))
                except Exception:
                    # raise ConnectionError("Server is closed or unavailable")
                    addTextToOutput(text_area, "Server is closed or unavailable")  
                    break
            print("out while")        
        except ConnectionError or ConnectionResetError:
            # raise ConnectionError("Server is closed or unavailable")
            addTextToOutput(text_area, "Server is closed or unavailable")
            print("Server is closed or unavailable")
            print("Closing broadcast channel")
            self.close()
        except Exception as e:
            print(f"Error: {e}")
    def sendCommand(self, command):
        try:
            self.clientSocket.sendall((command).encode('utf-8'))
            # return "OK"
        except Exception:
            print("server is closed or unavailable")
            # return "Server is closed or unavailable"

    def run(self, text_area):
        # set daemon = True to automatically closed broadcast channel when closing window
        self.receiveThread = threading.Thread(daemon = True,target = self.broadcast, args= (text_area, ))
        self.receiveThread.start()
        
    def close(self):
        # close connection to server
        self.runningBroadcast = False # force closing broadcast channel
        self.clientSocket.close()
        print("Closing client ...")
        
    def getHostName(self):
        return self.clientSocket.getsockname()   
class ClientFTPServer:
    def __init__(self, host, port):
        # self.address = address
        # self.authorizer = DummyAuthorizer()
        # self.authorizer.add_user(username, password, directory, perm='elradfmwMT')
        # self.handler = FTPHandler
        # self.handler.authorizer = self.authorizer
        # self.server = FTPServer(self.address, self.handler)
        self.host = host
        self.port = port
        self.connections = {}
    
    def clientHandle(self, clientSocket):
        try:
            clientMessage = clientSocket.recv(1024).decode('utf-8')
            JSONMessage = json.loads(clientMessage)
            payload = JSONMessage.get('PAYLOAD')
            filename = payload.get('filename')
            folder = payload.get('hostname') # hostname = folder
            current_path = os.getcwd()
            # print(f'{current_path}/{folder}/{filename}')
            print(f'CLient address: {clientSocket.getsockname()}')
            with open(f'{current_path}/{folder}/{filename}', 'rb') as file:
                file_data = file.read()
                clientSocket.sendall(file_data)
        except Exception as err:
            print(f"Catch exception: {err}")
    def start_server(self):
        # self.server.serve_forever()
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(5)
        print(f'File server is running on {self.host}/{self.port}')
        try:
            while True:
                try:
                    clientSocket, clientAddress = self.serverSocket.accept()
                    self.connections[clientAddress[1]] = clientSocket
                    print("a client connected")
                    clientHandler = threading.Thread(daemon = True,target = self.clientHandle, args = (clientSocket, ))
                    clientHandler.start()
                except OSError:
                    print("File server is closing")
                    break
        except Exception as err:
            print(f"Exception error: {err}")
    def close_server(self):
        # close FTP server
        # self.server.close_all()
        for key in self.connections:
            self.connections[key].close()
        
class ClientFTPClient:
    def __init__(self, host, port, localPort):
        # self.ftp = FTP()
        self.host = host
        self.port = port
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.host, self.port))
        self.localPort = localPort
        # self.fileName = ''
        # self.filePath = str(port) # Port is also used for folder name
    # def connect(self, host, port, username, password):
    #     self.ftp.connect(host, port)
    #     self.ftp.login(username, password)
    def getFile(self, filename):
        while True:
            receiveMessage = self.clientSocket.recv(1024)
            print(f'./{self.localPort}/{filename}')
            with open(f'./{self.localPort}/{filename}', 'wb') as file:
                file.write(receiveMessage)
                print('Downloaded successfully!')
                self.serverSocket.close()
                break
    def download_file(self, remote_folder, remote_filename):
        try:
            # Get remote file path
            # current_path = os.getcwd()
            # remote_folder_path = os.path.dirname(remote_file_path)
            # remote_folder_path_relative = os.path.relpath(remote_folder_path, current_path)
            # self.ftp.cwd('/'+remote_folder_path_relative)
            
            # print(remote_folder_path_relative)
            
            # start_time = time.time()
            # filename = os.path.basename(remote_file_path)  # Extract filename from remote path
            # local_file_path = os.path.join(local_folder_path, filename)
            # file_size = os.path.getsize(remote_file_path)
            # with open(local_file_path, 'wb') as file:
            #     self.ftp.retrbinary(f"RETR {filename}", file.write)
            # end_time = time.time()
            # self.ftp.quit()
            # return (f"File downloaded to '{local_file_path}' successfully. \nFile capacity: {file_size/1024}KB \nDownloading time: {(end_time - start_time)*1000} ms ")
            JSONMessage = convertJSONProtocol(f'retrieve {remote_folder} {remote_filename}')
            print(JSONMessage)
            self.clientSocket.sendall((JSONMessage).encode('utf-8'))
            self.getFile(remote_filename)
        except Exception as e:
            return (f"Error downloading file: {e}")
