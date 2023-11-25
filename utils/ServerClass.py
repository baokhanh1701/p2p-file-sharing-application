from .lib import *

pingSignal = threading.Event()

# buffer for printingLog in interface
printingLogWaiting = []
# save local list of every clients
saveLocalClient = {} 

def SearchLocalClient(filename):
  clientsFound = []
  for key in saveLocalClient:
    for file in saveLocalClient[key]:
      if(file == filename):
        clientsFound.append(key)
  return clientsFound

class Server:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.connections = {}
    self.FTPportClient = {}

  def clientHandle(self, clientSocket, clientAddress):
    while True:
      try:
        clientMessage = clientSocket.recv(1024).decode()
        """ 
          Valid command in client:
          - publish lname fname: lname(link), fname(name of file)
          - fetch fname: fetch some copy from target file
        """
        printingLogWaiting.append(f'{clientAddress} send to server: {clientMessage}')
        ## fetch case
        if  (clientMessage.split(' ')[0] == 'fetch'):
          fetchFile = clientMessage.split(' ')[1]
          clientsHaveFile = SearchLocalClient(fetchFile)
          returnMessage = ''
          if(len(clientsHaveFile) > 0):
            returnMessage = "Clients have file :"
            for client in clientsHaveFile:
              returnMessage += f"\n - {client} with ftpPort: {self.FTPportClient[client]}"
            returnMessage += "\n Which client you want to fetch from ?"
          else:
            returnMessage = f'There is no client having {fetchFile}'
          clientSocket.send(returnMessage.encode())
          printingLogWaiting.append(f'{clientAddress} want to fetch file name: {clientMessage.split(" ")[1]}')
        ## publish case
        elif (clientMessage.split(' ')[0] == 'publish'):
          saveLocalClient[clientAddress[1]].append(clientMessage.split(' ')[2])
          printingLogWaiting.append(f'link: {clientMessage.split(" ")[1]}')
          printingLogWaiting.append(f'filename: {clientMessage.split(" ")[2]}') 
        elif (clientMessage.split(' ')[0] == 'update'):
          saveLocalClient[clientAddress[1]].append(clientMessage.split(' ')[1])
          printingLogWaiting.append(f'update filename: {clientMessage.split(" ")[2]}') 
        elif(clientMessage == 'PONG'):
          time.sleep(0.5)
          pingSignal.set()
        elif(clientMessage.split(' ')[0] == 'FTPport'):
          ftpPort = clientMessage.split(' ')[1]
          self.FTPportClient[(clientAddress[1])] = (ftpPort)
        elif(clientMessage=="disconnect"):
          printingLogWaiting.append(f'{clientAddress} is disconnected')
          # clientSocket.close()
      except:
        break   
  
  def ping(self, hostname, textArea):
    try:
      pingMessage = "PING"
      startTime = time.time()
      hostnameSocket = self.connections[int(hostname)]
      hostnameSocket.send(pingMessage.encode())
      
      # Waiting for response
      pingSignal.wait()
      
      endTime = time.time()
      elapsedTime = endTime - startTime
      addTextToOutput(textArea, f"ping successfully, time: {elapsedTime*1000:.5f}ms")
    except Exception as err:
      print(f"Got error: {err}")
  
  def run(self):
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serverSocket.bind((self.host, self.port))
    self.serverSocket.listen(5)
    print(f'Server is running on {self.host}/{self.port}')
    try:
      while True:
        self.serverSocket.settimeout(1)
        try:
          clientSocket, clientAddress  = self.serverSocket.accept()
          self.connections[clientAddress[1]] = clientSocket
          clientSocket.send(f'{clientAddress} is your address'.encode())
          printingLogWaiting.append(f"{clientAddress} is connected")
          clientHandler = threading.Thread(target = self.clientHandle, args = (clientSocket, clientAddress))
          clientHandler.start()
          saveLocalClient[clientAddress[1]] = [] ## create server storage for clientAddress
        except socket.timeout:
          pass
    except KeyboardInterrupt:
      print('Keyboard Interrupted! The server is closed')
      # for conn in self.connections:
      #   conn.close()
      # self.serverSocket.close()
  
  def close(self):
    for key in self.connections:
      # print(key)
      self.connections[key].close()
    print(self.serverSocket)
    self.serverSocket.close()
      