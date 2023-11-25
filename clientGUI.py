from utils.lib import *
from utils.ClientClass import *

# Function to execute the command
def execute_command(client, command):
    """ 
        Valid command in client:
        - publish lname fname: lname(link), fname(name of file)
        - fetch fname: fetch some copy from target file
        - from ftpPort filename: confirm to get filename from ftpPort
    """
    try:
        opString = command.split(' ')[0]
        # fetch command
        if(opString == 'fetch' and len(command.split(' ')) == 2):
            # check if filename exist in local repository
            filename = command.split(' ')[1]
            if(filename in localRepository):
                addTextToOutput(text_area, f"{filename} has already existed in your repository")
            else:     
                client.sendCommand(command)
        elif(opString == 'publish' and len(command.split(' ')) == 3):
            """
                Check the path and file is valid
            """
            inputPath = command.split(' ')[1]
            inputFileName = command.split(' ')[2]
            filePathCheck = os.path.join(inputPath,inputFileName)
            if(os.path.exists(filePathCheck)):  
                if (not(inputFileName in localRepository)):
                    client.sendCommand(command)
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
        # from command to confirm fetch command
        elif(opString == "from" and len(command.split(' ')) == 3):
            # client.sendCommand(command)
            portname = command.split(' ')[1]
            filename = command.split(' ')[2]
            print(f"start fetching from {portname} {filename}")
            peer_client = ClientFTPClient()
            peer_client.connect('127.0.0.1', int(portname), 'user', '12345')
            peer_client.download_file(f"./{portname}/{filename}", f"./{sys.argv[1]}")
            # update client local repository
            # execute_command(f"update copy_{filename}")
            # update client local repository
            repository_listbox.insert(tk.END, f"copy_{filename}")
            client.sendCommand(f"update copy_{filename}")
        else:
            # text_area.insert(tk.END, "\n Your command is invalid, Please check again!!" )   
            addTextToOutput(text_area, "Your command is invalid, Please check again!!")
    except ConnectionError:
        # text_area.insert(tk.END, "\n" + "The connection to server is closed!!!")
        # text_area.insert(tk.END, "\n" + "Closing the window!!...")
        # asyncio.sleep(2)
        root.destroy()
        
def on_closing():
    ## interrupt connection here
    if messagebox.askokcancel("Quit", "Do you want to interrupt connection? "):
        # send to server disconnect signal
        client.sendCommand("disconnect")
        peer_server.close_server()
        peer_server_thread.join()
        client.close()
        root.destroy()
        

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print(f"File need one argument for ftp server port, find {len(sys.argv)-1} arguments")
        sys.exit()
    ftpPort = sys.argv[1]
    client = Client()
    
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
    server_address = ('127.0.0.1', ftpPort)
    username = 'user'
    password = '12345'
    directory = './' # Folder of a FTP server
    peer_server = ClientFTPServer(server_address, username, password, directory)
    peer_server_thread = threading.Thread(target=peer_server.start_server)
    peer_server_thread.start()

    # Entry for command input
    entry = tk.Entry(root, width=50)
    entry.pack(padx=10, pady=10)


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

    # Button to execute the command
    execute_button = tk.Button(root, text="Execute", command=lambda: execute_command(client, entry.get()))
    execute_button.pack(padx=10, pady=5)
    client.run(text_area)
    # Send ftp port to server for saving on server database
    client.sendCommand(f"FTPport {ftpPort}")
    root.mainloop()
