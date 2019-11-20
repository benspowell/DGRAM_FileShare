#  FilingCabinet

FilingCabinet is a peer-to-peer file sharing system written in python using DGRAM sockets. The application consists of two parts - client & server. The server runs on one machine and performs only simple directory management and communication. The clients connect to the server, inform it of what files they have to share, and either: "open their drawer" (wait to recieve a file request for another client) or try to download a file from another client. 

Developed at the Ohio State University by Ben Powell in Fall 2019 for an assignment in CSE 3461 (Computer Networking and Internet Technologies) with instructor David Ogle.

## User Manual
**System Requirements:**
  - Linux Operating System (should work on Windows and MacOS also, but has not been tested).
  - Python 2.7.5 (should work on other versions of python2, but has not been tested)
  
**To set up the project:**
  - Unzip folder or clone repository:
  <br>`$ unzip powell907_Lab2.zip -d FilingCabinet`<br>
  or
  <br>`$ git clone https://github.com/benspowell/FilingCabinet.git`<br>
  - Move into project folder:
  <br>`cd FilingCabinet`<br>
  
**Run the server-side application:**
  - If you're not already aware of the IP address of your machine, run `ifconfig` and take note of the public ipv4 address to share with clients.
  - Move into server folder:
  <br>`cd server`<br>
  - Run the program with python:
  <br>`python server.py` or `python server.py &` to run in background<br>

**Or run the client-side application:**
  - Move into client folder:
  <br>`cd client`<br>
  - Move files you wish to share into the `MyDrawer/` folder. For a sample, use my resume:
  <br>`curl http://benspowell.com/assets/Ben-Powell.pdf -o MyDrawer/resume.pdf`<br>
  - Run the program with python:
  <br>`python app.py`<br>
  - Follow the command line prompts.
  
## Features
This section explains the application's basic functionality from the perspective of the client and server. It is not necessary to read this section before running the application, as the user prompts are designed to be self-explanatory.

### Server Functionality
- When the server program is started, it initializes a IP-to-filename-list dictionary and a set of all availiable files, and immediately begins listening for packets from a client.
- When a client registers, the client's IP is added to the dictionary with an empty list.
- When a client informs the server of which files they have, the client's list is updated to reflect that.
- If a client requests a list or search, the server simply checks the set and responds with the answer.
- When a client requests a filename's locations, server searches the dictionary and builds a list of IPs that claim to have that file.
	- If no such clients are found, respond with an appropriate message and remove that file from the set.
	- If no information is held on that file, respont with an appropriate message.
- Client disconnects by sending a goodbye message - that client's IP is removed from the dictionary.
- Server must be closed with CTRL-C or CTRL-D to kill the process.

### Client Functionality
 - When a user runs the client app, they are prompted to input the location of the FilingCabinet server (in the form of its IP address). 
 - Next, the user's name is collected and a registration message is sent to the server.
 - The user is prompted with a list of the files contained in their `MyDrawer` folder, and asked to confirm that these files will be shared. This list can be updated later if the contents of the `MyDrawer` folder changes.
 - After the file names have been shared with the server, the client is provided with an option for the next command: 	
	 - `l` (list): check the cabinet directory for a list of available files.
	 - `s` (search): check for a certain file  in the cabinet.
	 - `g` (grab): get a file  from a drawer.
	 - `u` (update): update your drawer, sharing any new files with the cabinet.
	 - `o` (open): open your drawer, allowing people to get files from you.
	 - `q` (quit): quit the program.
 - The list, search, and update commands are self-explanatory and simply send the corresponding message to the server.
 - The open command directs the application to start listening for a message from another client. 
	 - If that message is received, and contains a request for a filename contained in the `MyDrawer` folder, the client program sends that file's contents in increments of 1024 bytes. 
	 - The program then continues to listen until it receives a `c` (close) command from the user.
 - The grab command prompts the user to enter a file name.
	 - A request is sent to the server to obtain the list of possible IP addresses to get the file from.
	 - After the list is recieved, the client loops through the list of IPs, requesting the file from each, until the file is recieved successfully.
 - The quit command exits the program after sending a goodbye message to the server.
 
## Message Protocol

The message protocol defines the type, syntax, semantics, and rules of the messages used in this application for communication between the clients and server. There are ten (10) types of messages. These messages along with their intended purpose and details are listed in the table below.

| Header          | Description                                                                                           | Sender | Reciever | Example                                             |
|-----------------|-------------------------------------------------------------------------------------------------------|--------|----------|-----------------------------------------------------|
| `iam`           | Register client in server record with initial message. <br> Expects a `message` response.             | Client | Server   | iam<br>Ben                                          |
| `ihave`         | Inform server of files held by the client, replacing previous record. Expects a `message` response    | Client | Server   | ihave<br>textfile.txt<br>music.mp3<br>document.docx |
| `list`          | Request list of potentially available files. Expects a `message` response.                            | Client | Server   | list                                                |
| `doyouhave`     | Search for specified file in server’s record. Expects a `message` response.                           | Client | Server   | doyouhave<br>music.mp3                              |
| `whereis`       | Request list of ip addresses for clients who have specified file. Expects a `filelocations` response. | Client | Server   | whereis<br>music.mp3                                |
| `goodbye`       | Inform server that client is going offline and will no longer be sharing files. Expects no response.  | Client | Server   | goodbye                                             |
| `giveme`        | Request a file from another client. Expects a `take` response.                                        | Client | Client   | giveme<br>music.mp3                                 |
| `take`          | Transfer [part of] a file to another client. Expects no response.                                     | Client | Client   | take<br>01010010<br>10111...                        |
| `message`       | Transmit a text message to a client. Expects no response.                                             | Server | Client   | message<br>hello there, friend.                     |
| `filelocations` | Transmit list of IP addresses for requested file. Expects no response.                                | Server | Client   | filelocations<br>12.34.56.78<br>140.254.61.94       |

## Disclaimer

This project was designed and submitted for a class assignment at the Ohio State University. All material in this project is the original work of the author, other than ideas and project requirements discussed in CSE 3461 lectures. To avoid academic misconduct, material from this project is not to be submitted for a class assignment by anyone other than the author.
