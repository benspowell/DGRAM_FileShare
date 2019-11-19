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
    response = "YOU SAID:\n"+data
    clientsock.sendto(response, addr)  
    print "* RESPONDED:\n", response