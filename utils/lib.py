# import all libraries for client and server

import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import shutil
import time
import socket
import threading
import sys
import json
# library for FTP server
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftplib import FTP



# add text to text_area and scroll to the end
def addTextToOutput(text_area, text):
  text_area.config(state = tk.NORMAL)
  text_area.insert(tk.END, f"\n {text}")
  text_area.see(tk.END)
  text_area.config(state = tk.DISABLED)
  
# analyze message to return JSON protocol  
def convertJSONProtocol(message):
  if(message.split(">")[0]!="message"):
    opString = message.split(' ')[0]
    returnJSONMessage = {}
    if(opString == 'publish' or opString == 'update'):
      path = message.split(' ')[1]
      filename = message.split(' ')[2]
      returnJSONMessage =  {
        "HEADER": opString,
        "TYPE": "REQUEST",
        "PAYLOAD": {
          "path": path,
          "filename": filename
        }
      }
    elif(opString == 'init'):
      ftpPort = message.split(' ')[1]
      returnJSONMessage = {
        "HEADER": opString,
        "TYPE": "REQUEST",
        "PAYLOAD": {
          "ftpPort": ftpPort 
        }
      }
    elif(opString == 'fetch'):
      filename = message.split(' ')[1]
      returnJSONMessage =  {
        "HEADER": opString,
        "TYPE": "REQUEST",
        "PAYLOAD": {
          "filename": filename
        }
      }
    elif(opString == 'ping' or opString == 'discover'):
      hostname = message.split(' ')[1]
      returnJSONMessage =  {
        "HEADER": opString,
        "TYPE": "REQUEST",
        "PAYLOAD": {
          "hostname": hostname
        }
      }
    elif(opString == 'retrieve'):
      hostname = message.split(' ')[1]
      filename = message.split(' ')[2]
      returnJSONMessage =  {
        "HEADER": opString,
        "TYPE": "REQUEST",
        "PAYLOAD": {
          "hostname": hostname,
          "filename": filename
        }
      }
    elif(opString == 'ping'):
      returnJSONMessage = {
        "HEADER": opString,
        "TYPE": "REQUEST",
        "PAYLOAD": None
      }
    else:
      pass
  # if message is response type, it will start with: "message> server/client >response"  
  else:
    startDest = message.split('>')[1]
    message = message.split('>')[2] # response part
    returnJSONMessage = {
      "HEADER": startDest,
      "TYPE": "RESPONSE",
      "PAYLOAD": {
        "message": message
      }
    }
  return json.dumps(returnJSONMessage, indent = None)