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
recipient = server_addr
s.sendto(msg, (recipient, PORT))
response = s.recv(1024)
print response

print "\nIn your local filesystem, you have a folder called MyDrawer."
print "\nAll files in your drawer will be shared with the cabinet directory.\n"
files = [f for f in listdir("MyDrawer/") if isfile(join("MyDrawer/", f))]

print "your files: ", files
raw_input("\nwhen you're ready to share, press enter...")

filestring=""
for f in files:
    filestring += f + "\\"
msg = "ihave\n" + filestring + "/"
print msg

while True:
    print "Availiable options:"
    print "     l (list): ask the cabinet directory for a list of availiable files."
    print "     s (search): check for a certain file in the cabinet."
    print "     g (get): get a file from a drawer."
    print "     u (update): update your drawer, sharing any new files with the cabinet."
    print "     o (open): open your drawer, allowing people to get files from you."
    
    command = raw_input("\n     >")

    if (command=="o"):
        while True:
            print "your drawer is now open for other clients to get your files"
            print "type 'close' to close your drawer."

            s.bind(('', PORT))
            data,addr = s.recvfrom(1024)  

            s.close
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            msg = "take\n"+"length\n"+"filedata"
            recipient = addr
            s.sendto(msg, (recipient, PORT))
            print "sent file x to ", addr

            break
    elif (command == "l"):
        msg = "list"
        recipient = server_addr
        s.sendto(msg, (recipient, PORT))

        response = s.recv(1024)
        print response 
    elif (command == "s"):
        msg = "doyouhave\n" + raw_input("what filename do you want to check for?")
        recipient = server_addr
        s.sendto(msg, (recipient, PORT))

        response = s.recv(1024)
        print response
    elif (command == "g"):
        msg = "whereis\n" + raw_input("what filename do you want to get")
        recipient = server_addr
        s.sendto(msg, (recipient, PORT))

        response = s.recv(1024)
        print response
    elif (command == "u"):
        print "\nAll files in your drawer will be shared with the cabinet directory.\n"
        files = [f for f in listdir("MyDrawer/") if isfile(join("MyDrawer/", f))]
        
        filestring=""
        for f in files:
            filestring += f + "\\"

        print "your files: ", filestring
        raw_input("\nwhen you're ready to share, press enter...")

        
        msg = "ihave\n" + filestring + "/"
        recipient = server_addr
        s.sendto(msg, (recipient, PORT))

        response = s.recv(1024)
        print response
        
s.close()

