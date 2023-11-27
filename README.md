# P2P File-sharing application

## Table of contents
 - [Description](#description)
 - [Current Workload](#current)
 - [Technology](#technology)
 - [Installation](#installation)
 - [Usage](#usage)

## Description
This application is used to build a simple client-server architecture. 

The clients can save some files in their local repository and send repository folder tree to server.

The server can save the folder tree of clients and connect them directly when a client require to fetch a file from another one.

## Current
Ver 0.2.1:
  - Optimize performance
  - Update file after fetching to local repository and server
  - Fix minor error

Ver 0.2.0:
  - Complete 4 basic commands
  - Code is not optimal
  - Did not catch exception yet

Ver 0.1.1: 
  - Build simple GUI for client and server with python GUI
  - Build class for client and server with multi-threading and can be executed along with GUI 

Ver 0.1.0:
  - Build in ReactJs
  - Cancel because JavaScript does not support multi-threading
 
## Technology
Ver 0.1.1:
  - GUI: tkinter
  - backend: python socket and threading, time, os

Ver 0.1.0:
  - GUI: ReactJS
  - backend: JavaScript

## Installation
```bash
git clone https://github.com/baokhanh1701/p2p-file-sharing-application.git
cd ./p2p-file-sharing-application
pip install -r requirements.txt
python3 serverGUI.py
```
Open new terminal to run client and replace PORTNUMBER as client FTP port
```bash
python3 clientGUI.py PORTNUMBER
```

## Usage
All command for client and server
1. Client
```bash
publish pathname filename
fetch filename
retrieve FTPportname filename
clear
```
2. Server
Server is running on 127.0.0.1/8080
```bash
ping hostname
discover hostname
clear
```

