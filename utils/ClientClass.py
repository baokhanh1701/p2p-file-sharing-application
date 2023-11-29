from .lib import *

# global text_area

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
            print(f'Client address: {clientSocket.getsockname()}')
            file_size = os.path.getsize(f'{current_path}/{folder}/{filename}')
            loaded = 0
            try:
                with open(f'{current_path}/{folder}/{filename}', 'rb') as file:
                    file_data = file.read(4096)
                    while file_data:
                        if not file_data:
                            print('end task')
                            break
                        else:
                            loaded += len(file_data)
                            # addTextToOutput(text_area, f'server is sending ...{round(loaded/file_size*100, 2)}%')
                            print(f'server is sending ...{round(loaded/file_size*100, 2)}%')
                            clientSocket.send(file_data)
                            file_data = file.read(4096)
                clientSocket.close()
                print("File sent, connection closed")
            except OSError as err:
                print(f'OSError: {err}')
        except Exception as err:
            print(f'{err}')
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
                    clientHandler = threading.Thread(target = self.clientHandle, args = (clientSocket, ))
                    clientHandler.start()
                except OSError:
                    print("File server is closing")
                    break
        except Exception as err:
            print(f"Exception error: {err}")
    def close_server(self):
        for key in self.connections:
            self.connections[key].close()
        self.serverSocket.close()
        
class ClientFTPClient:
    def __init__(self, host, port, localPort):
        # self.ftp = FTP()
        self.host = host
        self.port = port
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"{self.host}/{self.port} start to connect to 0.0.0.0/{self.port}")
        try:    
            self.clientSocket.connect((self.host, self.port))
        except ConnectionRefusedError:
            raise ConnectionRefusedError(f"Can not connect to remote server 0.0.0.0/{self.port}")
        self.localPort = localPort
    def getFile(self, filename):
        try:
            with open(f'./{self.localPort}/{filename}', 'wb') as file:
                while True:
                    receiveMessage = self.clientSocket.recv(4096)
                    print('client is getting ...')
                    if not receiveMessage:
                        # update filename to server
                        print('Get file successfully')
                        break
                    file.write(receiveMessage)
        except Exception as err:
            raise Exception(f"Exception in getFile: {err}")
        # self.serverSocket.close()
    def download_file(self, remote_folder, remote_filename):
        try:
            JSONMessage = convertJSONProtocol(f'retrieve {remote_folder} {remote_filename}')
            print(JSONMessage)
            self.clientSocket.sendall((JSONMessage).encode('utf-8'))
            self.getFile(remote_filename)
            return f"File {remote_filename} is download successfully"
        except Exception as e:
            return (f"Error downloading file: {e}")
