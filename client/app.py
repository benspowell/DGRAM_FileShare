import socket
from os import listdir
from os.path import isfile, join

PORT = 1998           # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream

print "Welcome!"
server_addr = raw_input("where is your filing cabinet? ")

msg = ""
recipient = ""

msg = "iam\n" + raw_input("who are you? ")
# recipient = server_addr
# s.sendto(msg, (recipient, PORT))
# response = s.recv(1024)

print "\nIn your local filesystem, you have a folder called MyDrawer."
print "\nAll files in your drawer will be shared with the cabinet directory.\n"
files = [f for f in listdir("MyDrawer/") if isfile(join("MyDrawer/", f))]

print "your files: ", files
raw_input("\nwhen you're ready to share, press enter...")

filestring=""
for f in files 
    filestring += f + "\\"
msg = "ihave\n" + filestring + "/"
print msg

while True:
    command = raw_input("what do you want to do?: ")

    if (command=="send"):
        msg = raw_input("what do you want to say? ")
        recipient = raw_input("to whom? ")
        s.sendto(msg, (recipient, PORT))
    elif (command=="recieve"):
        while True:  
            s.bind(('', PORT))
            data,addr = s.recv(1024)  
            print "Received ->", data
            print "from ", addr
            s.close
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            break
    elif (command == "register"):


s.close()

