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
    
    try:
      while True:
        clientMessage = clientSocket.recv(1024)
        clientJSONMessage = json.loads(clientMessage.decode('utf-8'))
        # print("receive message from client")
        # print(receiveData)
        """ 
          Valid command in client:
          - publish lname fname: lname(link), fname(name of file)
          - fetch fname: fetch some copy from target file
        """
        opString = clientJSONMessage.get('HEADER')
        payload = clientJSONMessage.get('PAYLOAD')
        printingLogWaiting.append(f'{clientAddress} send to server: {clientJSONMessage}')
        # continue
        ## fetch case
        if  (opString == 'fetch'):
          fetchFile = payload.get('filename')
          clientsHaveFile = SearchLocalClient(fetchFile)
          returnMessage = ''
          if(len(clientsHaveFile) > 0):
            returnMessage = "Clients have file :"
            for client in clientsHaveFile:
              returnMessage += f"\n  - {client} with ftpPort: {self.FTPportClient[client]}"
            returnMessage += "\n Which client you want to fetch from ?"
            # print(returnMessage)
          else:
            returnMessage = f'There is no client having {fetchFile}'
          returnClientJSONMessage = convertJSONProtocol(f"message>server>{returnMessage}")
          # print(returnClientJSONMessage)
          clientSocket.sendall((returnClientJSONMessage).encode('utf-8'))
          
          printingLogWaiting.append(f'{clientAddress} want to fetch file name: {fetchFile}')
        ## publish case
        elif (opString == 'publish'):
          saveLocalClient[clientAddress[1]].append(payload.get("filename"))
          printingLogWaiting.append(f'link: {payload.get("path")}')
          printingLogWaiting.append(f'filename: {payload.get("filename")}') 
        elif (opString== 'update'):
          saveLocalClient[clientAddress[1]].append(payload.get("filename"))
          printingLogWaiting.append(f'update filename: {payload.get("filename")}') 
        elif(opString == 'client' and payload.get("message") == 'pong'):
          print('server catch pong response')
          time.sleep(0.1)
          pingSignal.set()
        elif(opString == 'init'):
          ftpPort = payload.get("ftpPort")
          self.FTPportClient[(clientAddress[1])] = (ftpPort)
        # elif(clientMessage=="disconnect"):
        #   printingLogWaiting.append(f'{clientAddress} is disconnected')
          # clientSocket.close()
    except ConnectionResetError:
      time.sleep(1)
      # print("Client abruptly disconnected")
      printingLogWaiting.append(f'{clientAddress[1]} is disconnected from server')
      del saveLocalClient[clientAddress[1]] 
      # break
    except json.JSONDecodeError:
      # print(f"Catch error: {e}")   
      print("Invalid JSON received")
    except Exception as e:
      print(f"Error: {e}")
  def ping(self, hostname, textArea):
    try:
      jsonMessage = convertJSONProtocol(f"ping {hostname}")
      startTime = time.time()
      hostnameSocket = self.connections[int(hostname)]
      hostnameSocket.sendall((jsonMessage).encode('utf-8'))
      
      # Waiting for response
      if(pingSignal.wait(3)):
        endTime = time.time()
        elapsedTime = endTime - startTime
        addTextToOutput(textArea, f"ping successfully, time: {elapsedTime*1000:.5f}ms")
      else:
        addTextToOutput(textArea, f"ping failed, invalid response")
    except Exception as err:
      print(f"Got error: {err}")
  
  def run(self):
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serverSocket.bind((self.host, self.port))
    self.serverSocket.listen(5)
    print(f'Server is running on {self.host}/{self.port}')
    try:
      while True:
        # self.serverSocket.settimeout(1)
        try:
          clientSocket, clientAddress  = self.serverSocket.accept()
          self.connections[clientAddress[1]] = clientSocket
          # clientSocket.send(f'{clientAddress} is your address'.encode())
          printingLogWaiting.append(f"{clientAddress} is connected")
          clientHandler = threading.Thread(target = self.clientHandle, args = (clientSocket, clientAddress))
          clientHandler.start()
          saveLocalClient[clientAddress[1]] = [] ## create server storage for clientAddress
        except OSError:
          # print("Reconnecting...")
          print("Server is closing ...")
          break
    except KeyboardInterrupt:
      print('Keyboard Interrupted! The server is closed')
  
  def close(self):
    for key in self.connections:
      self.connections[key].close()
    # print(self.serverSocket)
    self.serverSocket.close()
      