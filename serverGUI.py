from utils.ServerClass import *
from utils.lib import *

class ServerGUI:
  def __init__(self):
    # Create signal for update real-time threading
    self.realTimeSignal = True
    
    # Create the main window and
    self.root = tk.Tk()
    self.root.title("Command Shell for server")

    # catch action closing server
    self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    # Entry for command input
    self.entry = tk.Entry(self.root, width = 50)
    self.entry.pack(padx=10, pady = 10)
    self.entry.bind("<Return>", lambda action: self.execute_command(self.entry.get()))
    
    # Text area to display command output
    self.textArea = scrolledtext.ScrolledText(self.root, wrap = tk.WORD, width = 60, height = 20)
    self.textArea.pack(padx = 10, pady = 10)
    addTextToOutput(self.textArea, f"The server is running on {host}/{port}")
    
    # Button to execute command
    # executeButton = tk.Button(self.root, text = "Execute", command = lambda: self.execute_command(self.entry.get()))
    # executeButton.pack(padx=10, pady = 5)
  
  def on_closing(self):
    if messagebox.askokcancel("Quit", "Do you want to stop server? "):
      server.close()
      # join all thread to main and close 
      self.realTimeSignal = False
      updateLogThread.join()
      # serverThread.join()
      self.root.destroy()
  
  def run(self):
    self.root.mainloop() 
    
  def execute_command(self, command):
    """
      2 commands valid in server command shell interpreter
      - discover hostname: discover the list of local files of the host named 'hostname'
      - ping hostname: live check the 'hostname'
    """
    self.entry.delete(0, tk.END)
    addTextToOutput(self.textArea, f"server${command}")
    if(command == "clear"):
        self.textArea.delete(1.0, tk.END)
    elif(len(command.split(' ')) == 2):
      opString = command.split(' ')[0]
      if(opString == 'discover'):
        clientAddress = command.split(' ')[1]
        try: 
          if(int(clientAddress) in saveLocalClient):
            if(len(saveLocalClient[int(clientAddress)]) > 0):
              addTextToOutput(self.textArea, f"The client {clientAddress} has following files:")
              for localFile in saveLocalClient[int(clientAddress)]:
                addTextToOutput(self.textArea, f" - {localFile}")
            else:
              addTextToOutput(self.textArea, f"This client did not upload any files")
          else:
            addTextToOutput(self.textArea, "This hostname does not exist in server")
        except KeyError:
          addTextToOutput(self.textArea, "Your hostname is invalid")
      elif(opString == 'ping'):
        hostname = command.split(' ')[1]
        pingThread = threading.Thread(target = server.ping, args = (hostname, self.textArea))
        pingThread.start()
      else:
        addTextToOutput(self.textArea, "This command is invalid")
    else:
      addTextToOutput(self.textArea, "This command is invalid")

  # update log from server per 0.1s  
  def updateRealtime(self):
    while self.realTimeSignal:
      time.sleep(0.01)
      if( len( printingLogWaiting ) != 0 ):
        for log in printingLogWaiting:
          addTextToOutput(self.textArea, log)
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
  