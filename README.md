# P2P File-sharing application

## Table of contents
 - [Description](#description)
 - [Current Commit](#current)
 - [Technology](#technology)
 - [Installation](#installation)
 - [Usage](#usage)

## Description
This application is used to build a simple client-server architecture. 

The clients can save some files in their local repository and send repository folder tree to server.

The server can save the folder tree of clients and connect them directly when a client require to fetch a file from another one.

## Current
Ver 0.2.2:
  - Fix error remote connection failed
  - Fix minor errors in formatting

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
Choose HOSTNAME = '0.0.0.0' and PORTNAME=8080
```bash
git clone https://github.com/baokhanh1701/p2p-file-sharing-application.git
cd ./p2p-file-sharing-application
python3 serverGUI.py HOSTNAME PORTNAME
```
Open new terminal to run client, choose your wifi ipv4 as IP_HOSTNAME
```bash
python3 clientGUI.py IP_HOSTNAME SERVER_PORT 
```

## Usage
All command for client and server
1. Client
```bash
publish pathname filename
fetch filename
retrieve FThostname filename
clear
```
2. Server <br>
Server is running on 127.0.0.1/8080
```bash
ping hostname
discover hostname
clear
```

