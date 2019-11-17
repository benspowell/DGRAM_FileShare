# Echo client program
import socket

PORT = 1998           # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream

print "Welcome!"
server_addr = raw_input("where is your filing cabinet? ")


command = raw_input("what is your header? ")

if (command=="send"):
    recipient = raw_input("to whom? ")
    message = raw_input("what do you want to say? ")
    s.sendto(message, (recipient, PORT))
elif (command=="recieve"):
    while True:  
        s.bind(('', PORT))
        data,addr = s.recv(1024)  
        print "Received ->", data
        print "from ", addr
        s.close
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        break



s.close()


