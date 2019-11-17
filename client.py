# Echo client program
import socket

HOST = 'localhost'   # The remote host
PORT = 5000           # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream
msg = 'Hello, world.'
s.sendto(msg, (HOST, PORT))
data = s.recv(1024)
s.close()
print "Received -> ", repr(data)