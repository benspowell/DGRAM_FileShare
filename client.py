# Echo client program
import socket

HOST = 'file.powell.mx'   # The remote host
PORT = 5000           # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream

command = raw_input("what is your command? ")

if (command=="send"):
    recipient = raw_input("to whom? ")
    message = raw_input("what do you want to say? ")
    s.sendto(message, (recipient, PORT))
elif (command=="recieve"):
    while True:  
        s.bind(('', PORT))
        data, addr = s.recvfrom(1024)  
        print "Received ->", data
        print "from ", addr
        break

s.close()


