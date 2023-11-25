# import all libraries for client and server

import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import shutil
import time
import socket
import threading
import sys
# library for FTP server
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftplib import FTP



# add text to text_area and scroll to the end
def addTextToOutput(text_area, text):
  text_area.insert(tk.END, f"\n {text}")
  text_area.see(tk.END)