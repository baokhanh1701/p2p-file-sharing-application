from utils.ClientClass import *
from tkinter import scrolledtext
import os

# Function to execute the command
def execute_command(client, command):
    """ 
        Valid command in client:
        - publish lname fname: lname(link), fname(name of file)
        - fetch fname: fetch some copy from target file
    """
    try:
        if(command.split(' ')[0] == 'fetch' and len(command.split(' ')) == 2):
            client.sendCommand(command)
            output = "Command is executing... "
            text_area.insert(tk.END, "\n" + output)
        elif(command.split(' ')[0] == 'publish' and len(command.split(' ')) == 3):
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
                    output = "The file is added to repository successfully!! "
                    text_area.insert(tk.END, "\n" + output)
                else:
                    text_area.insert(tk.END, f"\n The file '{inputFileName}' exists in local repository.")
            else:
                text_area.insert(tk.END, f"\n The file '{inputFileName}' exists in the directory '{inputPath}'.")
        else:
            text_area.insert(tk.END, "\n Your command is invalid, Please check again!!" )   
        
    except ConnectionError:
        # text_area.insert(tk.END, "\n" + "The connection to server is closed!!!")
        # text_area.insert(tk.END, "\n" + "Closing the window!!...")
        # asyncio.sleep(2)
        root.destroy()

if __name__ == "__main__":
    client = Client()
    
    # Create the main window
    root = tk.Tk()
    root.title("Command Shell for client")

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

    # Adding some sample repositorys to the list
    localRepository = []
    for repository in localRepository:
        repository_listbox.insert(tk.END, repository)

    # Button to execute the command
    execute_button = tk.Button(root, text="Execute", command=lambda: execute_command(client, entry.get()))
    execute_button.pack(padx=10, pady=5)
    client.run(text_area)
    # sys.excepthook = lambda: root.destroy() // exception for broadcast
    root.mainloop()
