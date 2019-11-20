import select, socket, sys, Queue, os
import socket
from os import listdir
from os.path import isfile, join

def sendthis(s, msg, recipient):
    PORT = 1998
    #message logging
    print "\n------sending------"
    print msg
    print "-------------------\n"
    #message logging
    s.sendto(msg, (recipient, PORT))

def recvresp(s):
    s.settimeout(10.0)
    try:
        response,addr = s.recvfrom(1024)
    except socket.timeout:
        print "socket timed out :("
        response = false
    print "\n-----recieved------"
    print response 
    print "-------------------\n"
    return response

def collectFiles():
    files = [f for f in listdir("MyDrawer/") if isfile(join("MyDrawer/", f))]

    fileString=""

    for f in files:
        fileString += "\n" + f

    return fileString

def sendFile(s, filename, recipient):
    f = open("MyDrawer/"+filename, "rb")
    fileData = f.read()
    s.sendto(fileData,(recipient, 1998))
    f.close

def recvFile(s, filename):
    f.open("MyDrawer/"+filename, "wb")
    s.settimeout(10.0)
    try:
        data,addr = s.recvfrom()
        recv = true
    except socket.timeout:
        print "socket timed out :("
        recv = false

    if recv:
        f.write(data)

    f.close
    return recv

HOST= ''
PORT = 1998            # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream
s.bind((HOST, PORT))

# Get server address
print "Welcome!"
server_addr = raw_input("where is your filing cabinet? ")

# Register user with server
print "ok, registering you with "+server_addr+"\n"
msg = "iam\n" + raw_input("     who are you? ")
sendthis(s, msg, server_addr)
recvresp(s)

# Collect files
print "\nIn your local filesystem, you have a folder called MyDrawer."
print "\nAll files in your drawer will be shared with the cabinet directory.\n"
filestring = collectFiles()
print "your files:\n", filestring

# Send file names to server
raw_input("\nwhen you're ready to share, press enter...")
sendthis(s, "ihave" + filestring, server_addr)
recvresp(s)

while True:
    print "\nAvailiable options:"
    print "     l (list): ask the cabinet directory for a list of availiable files."
    print "     s (search): check for a certain file in the cabinet."
    print "     g (grab): get a file from a drawer."
    print "     u (update): update your drawer, sharing any new files with the cabinet."
    print "     o (open): open your drawer, allowing people to get files from you."
    command = raw_input("\n     >")
    print

    if (command=="o"): # OPEN COMMAND: waits for another user to request a file
        print "your drawer is now open for other clients to get your files!"
        print "type 'c' and press enter to close your drawer." 
        
        inputs = [s, sys.stdin]
            
        while inputs:
            if (command =="c"): break
            readable, writable, exceptional = select.select(inputs, inputs, inputs)
            for i in readable:
                if i is s:
                    response, addr = s.recvfrom()
                    # sendthis(s, "take\n"+"length\n"+"filedata", addr[0])
                    fn = response.split()[1]
                    sendFile(s, fn, addr)
                elif i is sys.stdin:
                    command = raw_input()
                    if (command == "c"):
                        print "closing drawer..."
                        break
            for ex in exceptional:
                print 'something bad happened. :('
                break 
    elif (command == "l"): # LIST COMMAND: ask server to list files
        sendthis(s, "list", server_addr)
        recvresp(s)

    elif (command == "s"): # SEARCH COMMAND: ask server to search for a certain file
        msg = "doyouhave\n" + raw_input("what filename do you want to check for? ")
        sendthis(s, msg, server_addr)
        recvresp(s)

    elif (command == "g"): # GRAB COMMAND: ask server for file location, then try to get file
        fileiwant = raw_input("what filename do you want to get? ")
        msg = "whereis\n" + fileiwant
        sendthis(s, msg, server_addr)
        
        ips = recvresp(s).split()
        if (ips.pop(0) == "message"):
            print ips.pop(0)
        else:
            for ip in ips:
                msg = "giveme\n"+fileiwant
                sendthis(s,msg,ip)
                if recvFile(s, "abcd"):
                    break

    elif (command == "u"): # UPDATE COMMAND: update this user's shared files
        print "\nAll files in your drawer will be shared with the cabinet directory.\n"

        filestring = collectFiles()
        print "your files:\n", filestring

        raw_input("\nwhen you're ready to share, press enter...")
        sendthis(s, "ihave\n" + filestring, server_addr)
        recvresp(s)

s.close()
