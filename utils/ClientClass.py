from .lib import *



class Client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8080
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.runningBroadcast = True # signal for broadcast function
        # self.clientSocket.bind(('0.0.0.0', int(sys.argv[2])))
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
    def __init__(self, address, username, password, directory):
        self.address = address
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_user(username, password, directory, perm='elradfmwMT')
        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer
        self.server = FTPServer(self.address, self.handler)

    def start_server(self):
        self.server.serve_forever()
    
    def close_server(self):
        # close FTP server
        self.server.close_all()
        
class ClientFTPClient:
    def __init__(self):
        self.ftp = FTP()

    def connect(self, host, port, username, password):
        self.ftp.connect(host, port)
        self.ftp.login(username, password)

    def download_file(self, remote_file_path, local_folder_path):
        try:
            start_time = time.time()
            filename = os.path.basename(remote_file_path)  # Extract filename from remote path
            local_file_path = os.path.join(local_folder_path, filename)
            file_size = os.path.getsize(remote_file_path)
            with open(local_file_path, 'wb') as file:
                self.ftp.retrbinary(f"RETR {remote_file_path}", file.write)
            end_time = time.time()
            return (f"File downloaded to '{local_file_path}' successfully. \nFile capacity: {file_size/1024}KB \nDownloading time: {(end_time - start_time)*1000} ms ")
        
        except Exception as e:
            return (f"Error downloading file: {e}")