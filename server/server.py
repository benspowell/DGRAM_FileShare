import socket

HOST = ''
PORT = 1998
clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream
clientsock.bind((HOST, PORT))
print "Waiting for packets..."

IPsToFiles = {}
allFiles = {}

while True:  
    data, addr = clientsock.recvfrom(1024)  
    print
    print "\n* RECIEVED:\n", data  
    print "* FROM: ", addr

    dataList = data.split("\n")

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
            # Get the file locationS TODO
            loc = ""
            for f in IPsToFiles: 
                if dataList[0] in IPsToFiles[f]: 
                    loc += "\n"+f[0]
            response = "filelocations" + loc
        else:
            response = "message\nI don't know that file's location!"
    clientsock.sendto(response, addr)  
    print "* RESPONDED:\n", response
