from .lib import *

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
                # check for ping message
                if(receivedMessage == "PING"):
                    returnPingMessage = "PONG"
                    try:
                        time.sleep(0.5)
                        self.clientSocket.send(returnPingMessage.encode())
                    except ConnectionError:
                        raise ConnectionError("Server is closed or unavailable")
                # check for fetch message
                # elif(receivedMessage.split(' ')[0] == "fetching"):
                #     portname = receivedMessage.split(' ')[2]
                #     filename = receivedMessage.split(' ')[1]
                #     print(f"receive fetching command {portname} {filename}")
                #     peer_client = ClientFTPClient()
                #     peer_client.connect('127.0.0.1', int(portname), 'user', '12345')
                #     peer_client.download_file(f"./{portname}/{filename}", f"./{sys.argv[1]}")
                # other message will be printed to output directly
                else:
                    addTextToOutput(text_area, receivedMessage)
                    
        except ConnectionError as err:
            raise ConnectionError("Server is closed or unavailable")
            # sys.__excepthook__(type(err), err, err.__traceback__)
    def sendCommand(self, command):
        try:
            self.clientSocket.send(command.encode())
        except ConnectionError:
            raise ConnectionError("Server is closed or unavailable")
        
    def run(self, text_area):
        self.receiveThread = threading.Thread(target = self.broadcast, args= (text_area, ))
        self.receiveThread.start()
        
    def close(self):
        # close connection to server
        # join receiveThread
        self.clientSocket.close()
        self.receiveThread.join()
        
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
            filename = os.path.basename(remote_file_path)  # Extract filename from remote path
            local_file_path = os.path.join(local_folder_path, "copy_" + filename)
            with open(local_file_path, 'wb') as file:
                self.ftp.retrbinary(f"RETR {remote_file_path}", file.write)
            print(f"File downloaded to '{local_file_path}' successfully.")
        except Exception as e:
            print(f"Error downloading file: {e}")