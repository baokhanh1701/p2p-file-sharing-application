from utils.ServerClass import *
from tkinter import scrolledtext


# print (saveLocalClient)
# print (printingLogWaiting)

class ServerGUI:
  def __init__(self):
    # Create the main window and
    self.root = tk.Tk()
    self.root.title("Command Shell for server")
  
    # Entry for command input
    entry = tk.Entry(self.root, width = 50)
    entry.pack(padx=10, pady = 10)
    
    # Text area to display command output
    self.textArea = scrolledtext.ScrolledText(self.root, wrap = tk.WORD, width = 60, height = 20)
    self.textArea.pack(padx = 10, pady = 10)
    self.textArea.insert(tk.END, "\n The server is running on {}/{}".format(host, port))
    
    # Button to execute command
    executeButton = tk.Button(self.root, text = "Execute", command = lambda: self.execute_command(entry.get()))
    executeButton.pack(padx=10, pady = 5)
  
  def run(self):
    self.root.mainloop() 
    
  def execute_command(self, command):
    """
      2 commands valid in server command shell interpreter
      - discover hostname: discover the list of local files of the host named 'hostname'
      - ping hostname: live check the 'hostname'
    """
    if(len(command.split(' ')) == 2):
      opString = command.split(' ')[0]
      if(opString == 'discover'):
        clientAddress = command.split(' ')[1]
        try: 
          if(int(clientAddress) in saveLocalClient):
            if(len(saveLocalClient[int(clientAddress)]) > 0):
              self.textArea.insert(tk.END, "\nThe client {} has following files: ".format(clientAddress))
              for localFile in saveLocalClient[int(clientAddress)]:
                self.textArea.insert(tk.END, "\n - {}".format(localFile))
            else:
              self.textArea.insert(tk.END, "\n This client did not upload any files")
          else:
            self.textArea.insert(tk.END, "\n This hostname does not exist in server")
        except KeyError:
          self.textArea.insert(tk.END, "\n Your hostname is invalid")
      elif(opString == 'ping'):
        hostname = command.split(' ')[1]
        pingThread = threading.Thread(target = server.ping, args = (hostname, self.textArea))
        # pingStatus, responseTime = server.ping(hostname)
        pingThread.start()
      else:
        self.textArea.insert(tk.END, "\n The command is invalid")  
    else:
      self.textArea.insert(tk.END, "\n The command is invalid")  
    
    
  def updateRealtime(self):
    while True:
      time.sleep(0.5)
      if(len( printingLogWaiting ) != 0):
        for log in printingLogWaiting:
          self.textArea.insert(tk.END, "\n" + log)
        printingLogWaiting.clear()
      
      

if __name__ == "__main__":
  host = "127.0.0.1"
  port = 8080
  server = Server(host, port)
  gui = ServerGUI()
  # server = ''
  
  serverThread = threading.Thread(target = server.run)
  # update log from server per 0.5 second
  updateLogThread = threading.Thread(target = gui.updateRealtime)
  
  serverThread.start()
  updateLogThread.start()
  
  
  gui.run()
  