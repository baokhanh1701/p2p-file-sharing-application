from utils.ServerClass import *
import tkinter as tk
import threading
from tkinter import scrolledtext
import time

def execute_command(server, command):
  pass


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
    executeButton = tk.Button(self.root, text = "Execute", command = lambda: execute_command(server, entry.get()))
    executeButton.pack(padx=10, pady = 5)
  
  def run(self):
    self.root.mainloop() 
    
  def updateRealtime(self):
    while True:
      time.sleep(0.5)
      print (printingLogWaiting, flush=True)
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
  