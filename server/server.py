import socket

HOST = ''
PORT = 1998
clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream
clientsock.bind((HOST, PORT))
print "Waiting for packets..."

while True:  
    data, addr = clientsock.recvfrom(1024)  
    print
    print "\n* RECIEVED:\n", data  
    print "* FROM: ", addr

    dataList = data.split("\n")

    if (dataList[0]=="iam"):
        # Register the user TODO
        response = "message\nHello, "+dataList[1]+". Welcome to FilingCabinet."
    elif (dataList[0]=="ihave"):
        # Register the user's files TODO
        response = "message\nI got your files. Thanks."
    elif (dataList[0]=="doyouhave"):
        # Check if I have that file on record TODO
        response = "message\nchecking..."
    elif (dataList[0]=="list"):
        # Send the list of files TODO
        response = "message\nHere's the list:\na\nb\nc"
    elif (dataList[0]=="whereis"):
        # Make sure I have that file TODO
        # Get the file locationS TODO
        response = "filelocations\na\nb\nc"
        
    clientsock.sendto(response, addr)  
    print "* RESPONDED:\n", response