import socket
import threading
import time
import tkinter as tk

pingSignal = threading.Event()

listFileSample = [
  'test.txt',
  'image.jpg',
  'music.mp3',
  'video.mp4'
]

# buffer for printingLog in interface
printingLogWaiting = []
# save local list of every clients
saveLocalClient = {} 

class Server:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.connections = {}
     

  def clientHandle(self, clientSocket, clientAddress):
    while True:
      try:
        clientMessage = clientSocket.recv(1024).decode()
        """ 
          Valid command in client:
          - publish lname fname: lname(link), fname(name of file)
          - fetch fname: fetch some copy from target file
        """
        # print('{} send to server: {}'.format(clientAddress, clientMessage))
        printingLogWaiting.append('{} send to server: {}'.format(clientAddress, clientMessage))
        ## fetch case
        if  (clientMessage.split(' ')[0] == 'fetch'):
          returnMessage = 'Available files: {}'.format(listFileSample)
          clientSocket.send(returnMessage.encode())
          printingLogWaiting.append('{} want to fetch file name: {}'.format(clientAddress, clientMessage.split(' ')[1]))
        ## publish case
        elif (clientMessage.split(' ')[0] == 'publish'):
          # print('link: {}'.format(clientMessage.split(' ')[1]))
          # print('filename: {}'.format(clientMessage.split(' ')[2]))
          saveLocalClient[clientAddress[1]].append(clientMessage.split(' ')[2])
          print(saveLocalClient)
          printingLogWaiting.append('link: {}'.format(clientMessage.split(' ')[1]))
          printingLogWaiting.append('filename: {}'.format(clientMessage.split(' ')[2])) 
        elif(clientMessage == 'PONG'):
          time.sleep(0.5)
          pingSignal.set()
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
      # print("ping successfully, time: {}", elapsedTime)
      textArea.insert(tk.END, "\n ping successfully, time: {:.5f}ms".format(elapsedTime*1000))
    except Exception as err:
      print("Got error: {}".format(err))
  
  def run(self):
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serverSocket.bind((self.host, self.port))
    self.serverSocket.listen(5)
    print('Server is running on {}/{}'.format(self.host, self.port))
    try:
      while True:
        self.serverSocket.settimeout(1)
        try:
          clientSocket, clientAddress  = self.serverSocket.accept()
          self.connections[clientAddress[1]] = clientSocket
          clientSocket.send('{} is your address'.format(clientAddress).encode())
          print('{} is connected'.format(clientAddress))
          clientHandler = threading.Thread(target = self.clientHandle, args = (clientSocket, clientAddress))
          clientHandler.start()
          saveLocalClient[clientAddress[1]] = [] ## create server storage for clientAddress
        except socket.timeout:
          pass
    except KeyboardInterrupt:
      print('Keyboard Interrupted! The server is closed')
      for conn in self.connections:
        conn.close()
      self.serverSocket.close()
      