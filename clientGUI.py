from utils.lib import *
from utils.ClientClass import *

# Function to execute the command
def execute_command(client, command):
    entry.delete(0, tk.END)
    hostname = client.getHostName()
    """ 
        Valid command in client:
        - publish lname fname: lname(link), fname(name of file)
        - fetch fname: fetch some copy from target file
        - from ftpPort filename: confirm to get filename from ftpPort
    """
    addTextToOutput(text_area, f"user-{hostname[1]}${command}")
    # convert command string to json
    jsonProtocolCommand = ''
    # print(jsonProtocolCommand)
    
    # check command validation before sending to server
    opString = command.split(' ')[0]
    
    if(command == "clear"):
        text_area.delete(1.0, tk.END)
    # fetch command
    elif(opString == 'fetch' and len(command.split(' ')) == 2):
        # check if filename exist in local repository
        filename = command.split(' ')[1]
        if(filename in localRepository):
            addTextToOutput(text_area, f"{filename} has already existed in your repository")
        else:     
            jsonProtocolCommand = convertJSONProtocol(command)
            client.sendCommand(jsonProtocolCommand)
    #publish command
    elif(opString == 'publish' and len(command.split(' ')) == 3):
        """
            Check the path and file is valid
        """
        inputPath = command.split(' ')[1]
        inputFileName = command.split(' ')[2]
        filePathCheck = os.path.join(inputPath,inputFileName)
        if(os.path.exists(filePathCheck)):  
            if (not(inputFileName in localRepository)):
                jsonProtocolCommand = convertJSONProtocol(command)
                client.sendCommand(jsonProtocolCommand)
                localRepository.append(inputFileName)
                repository_listbox.insert(tk.END, inputFileName)
                addTextToOutput(text_area, "The file is added to repository successfully!! ")
                # Copy file to general folder
                shutil.copy(filePathCheck, f"./{ftpPort}")
            else:
                # text_area.insert(tk.END, f"\n The file '{inputFileName}' exists in local repository.")
                addTextToOutput(text_area, f"The file '{inputFileName}' exists in local repository.")
        else:
            addTextToOutput(text_area, f"The file '{inputFileName}' does not exist in the directory '{inputPath}'.")
    
    # retrieve command to confirm hostname selection
    elif(opString == "retrieve" and len(command.split(' ')) == 3):
        portname = command.split(' ')[1]
        filename = command.split(' ')[2]
        # Must check whether filename is fetched or not
        if(filename in localRepository):
            addTextToOutput(text_area, "you has fetched this file before")
        else:
            print(f"start fetching from {portname} {filename}")
            peer_client = ClientFTPClient()
            peer_client.connect('127.0.0.1', int(portname), 'user', '12345')
            downloadMessage = peer_client.download_file(f"./{portname}/{filename}", f"./{ftpPort}")
            # update client local repository
            localRepository.append(f"{filename}")
            repository_listbox.insert(tk.END, f"{filename}")
            JSONcommand = convertJSONProtocol(f"update ./{ftpPort} {filename}")
            client.sendCommand(JSONcommand)
            addTextToOutput(text_area, downloadMessage)
    else:
        # text_area.insert(tk.END, "\n Your command is invalid, Please check again!!" )   
        addTextToOutput(text_area, "Your command is invalid, Please check again!!")
        
def on_closing():
    ## interrupt connection here
    if messagebox.askokcancel("Quit", "Do you want to interrupt connection? "):
        # send to server disconnect signal
        # client.sendCommand("disconnect")
        # close FTP server
        peer_server.close_server()
        peer_server_thread.join()
        # Close connection between client and server
        client.close()
        # Close window
        root.destroy()
        

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        print(f"File need 2 arguments for server host and port, find {len(sys.argv)-1} arguments")
        sys.exit()
    # get ftp port from argument
    host = sys.argv[1] # define host for connecting server
    port = int(sys.argv[2])
    try:
        client = Client(host, port)
    except ConnectionError:
        print("Can not connect to server")
        sys.exit()
        
    ftpPort = client.getHostName()[1] % 100
    
    #Create folder for local repository
    folder_path = os.path.join(os.getcwd(), f"{ftpPort}")
    if(not os.path.exists(folder_path)):
        os.mkdir(folder_path)
    
    # Create the main window
    root = tk.Tk()
    root.title("Command Shell for client")
    
    # Catch action user close window
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Create FTP Server
    server_address = ('0.0.0.0', ftpPort)
    username = 'user'
    password = '12345'
    directory = './' # Folder of a FTP server
    peer_server = ClientFTPServer(server_address, username, password, directory)
    peer_server_thread = threading.Thread(target=peer_server.start_server)
    peer_server_thread.start()

    # Entry for command input
    entry = tk.Entry(root, width=50)
    entry.pack(padx=10, pady=10)
    entry.bind("<Return>", lambda action: execute_command(client, entry.get()))

    # Frame for user list components
    repository_frame = tk.Frame(root)
    repository_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    # Text area to display command output
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    text_area.pack(padx=10, pady=10)

    # Label for repository list
    repository_label = tk.Label(repository_frame, text="Local repository")
    repository_label.pack(padx=10, pady=5)

    # Listbox to display the repository list
    repository_listbox = tk.Listbox(repository_frame)
    repository_listbox.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

    # Adding some sample repository to the list
    localRepository = []
    for repository in localRepository:
        repository_listbox.insert(tk.END, repository)
 
    client.run(text_area)
    # Send ftp port to server for saving on server database
    initMessage = convertJSONProtocol(f"init {ftpPort}")
    client.sendCommand(initMessage)
    
    root.mainloop()
