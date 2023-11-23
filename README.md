# P2P File-sharing application

## Table of contents
 - [Description](#description)
 - [Current Workload](#current)
 - [Technology](#technology)
 - [Installation](#installation)
 - [Contributing](#contributing)

## Description
This application is used to build a simple client-server architecture. 

The clients can save some files in their local repository and send repository folder tree to server.

The server can save the folder tree of clients and connect them directly when a client require to fetch a file from another one.

## Current Workload
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
python3 serverGUI.py
```
Open new terminal to run client
```bash
python3 clientGUI.py
```

## Contributing

