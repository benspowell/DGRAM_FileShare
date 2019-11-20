import socket

# Set up socket
HOST = '' 
PORT = 1998 # Same port used in client.
clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsock.bind((HOST, PORT))
print "HELLO! YOU ARE RUNNING THE SERVER FOR THE FilingCabinet APP!\n"

# Dictionary containing IPs as keys and list of their filenames as values.
IPsToFiles = {}

# Set containing all the availiable files
allFiles = set()

print "WAITING FOR PACKETS..."
while True:  
    # Listen for packets from clients
    data, addr = clientsock.recvfrom(1024)

    # Received a packet, print details
    print "\n\n----RECIEVED---------------\n", data  
    print "----FROM-------------------\n", addr

    # Split packet into components based on \n delimiter
    dataList = data.split("\n")

    # First line is the header. Pop it off and do something based on value
    header = dataList.pop(0)

    if (header == "iam"):
        # Register the user
        IPsToFiles[addr] = []
        response = "message\nHello, "+dataList[0]+". Welcome to FilingCabinet."

    elif (header == "ihave"):
        # Register the user's files
        for f in dataList:
            IPsToFiles[addr].append(f)
            allFiles.add(f)
        response = "message\nI got your files. Thanks."
    elif (header == "doyouhave"):
        # Check if I have that file on record
        if dataList[0] in allFiles:
            response = "message\nYes! I have that file on record."
        else:
            response = "message\nNO. I do not have that file on record."
            
    elif (header == "list"):
        # Send the list of files
        response = "message\nHere's the list:\n"+'\n'.join(allFiles)
    elif (header == "whereis"):
        # Make sure I have that file
        if dataList[0] in allFiles:
            # Get the file locations
            loc = ""
            for f in IPsToFiles: 
                # This ip has the file
                if dataList[0] in IPsToFiles[f]: 
                    # Add it to the location string
                    loc += "\n"+f[0]
            response = "filelocations" + loc

            # File not found in any IP's list
            if (loc==""):
                # Remove it from list
                allFiles.remove(dataList[0])
                # Inform client
                response = "message\nSORRY, that file is no longer available."
        else:
            # I dont have info on that file
            response = "message\nI don't know that file's location!"
    elif (header == "goodbye"):
        # Remove that client's entry
        IPsToFiles.pop(addr, None)

    # Send and log response
    clientsock.sendto(response, addr)  
    print "----RESPONDED--------------\n", response
    print "----TO-------------------\n", addr