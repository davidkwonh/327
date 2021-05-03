"""
SERVER SIDE: deals with uploading files for other peers
"""

import socket 
import threading 
import sys
import time
import client
import P2P
import pickle
import os

BYTE_SIZE = 1024
HEADERSIZE = 10
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
PEER_BYTE_DIFFERENTIATOR = b'\x11' 
REQUEST_STRING = "req"

class Server: 
    """
    constructor for server
    """

    def __init__(self):
        try:
            # define a socket
            # (family=AF_INET, type=SOCK_STREAM)
            # AF_INET is pair (host, port) where host is hostname in domain and port is port number being used
            # SOCK_STREAM is default type for socket which is pretty much TCP. Keeps connection until terminated. 
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # (level, optname, value)
            # level: SOL_SOCKET meaning manipulate options at the socket API level
            # optname: SO_REUSEADDR meaning to reuse socket address in case of client closing 
            # value: integer representing buffer 
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # make a list of connections
            self.connections = []

            # make a list of peers 
            self.peers = []

            # creating starting DHT for server
            self.dht = self.fileList()

            # bind the socket to HOST 127.0.0.1, and PORT 5000
            self.s.bind((HOST, PORT))

            # listen for connection
            # the number of unaccepted connections that the system will allow before refusing new connects: 1
            self.s.listen(1)

            # output if the server is running
            print("-" * 3 + "Server Running"+ "-" * 3)
            
            self.run()

        except KeyboardInterrupt as e:
            print("INTERRUPT INSIDE OF INIT")
            sys.exit()

    """
    code that compares the client dht to that of the server based off three things by the following priority
    1.filename = key
    2.hash value (if the keys are the same but different hash values)  
    3.most recent timestamp (the more recent file will be the one sent to the other machine)]
    """
    def comparedht(self, clientdht):

        # initiate a temp dictionary to hold file
        #tempDict = {}

         # start comparing files
        for filename in clientdht.keys():
            # same name:
            # keys() returns a list of all the available keys in the clientdht
            if filename in self.dht.keys():
                # pass if the files have the same hash value
                if self.dht[filename][0] == clientdht[filename][0]:
                    # No changes were made
                    # move on to the next file
                    continue

                else:
                    # Need to compare time stamps
                    if self.dht[filename][1] > clientdht[filename][1]:
                        # Server has most up to date
                        # Send file to client
                        self.s.send("r".encode('utf-8'))
                        time.sleep(1)
                        self.s.send(filename.encode('utf-8'))
                        self.s.send(self.dht[filename])

                    else: 
                        # Client has most up to date
                        # Request file from client
                        self.s.send("s".encode('utf-8'))
                        time.sleep(1)

            else: 
                # File not in server directory
                # Client sends file over
                self.connections[0].send("s".encode('utf-8'))
                time.sleep(1)
                self.connections[0].send(filename.encode('utf-8'))

                fileContent = self.connections[0].recv(BYTE_SIZE)

                # write data to directory
                P2P.makefile(fileContent)

        # adding leftover file in client node to the temp dictionary
        for filename in self.dht:
            if filename not in clientdht.keys():
                # Client needs file from server
                # server sends file to client
                self.s.send("r".encode('utf-8'))
                time.sleep(1)
                self.s.send(filename)
        
        self.s.send('q'.encode('utf-8'))
        self.fileList() # updating server dht

                
    # a function to return a dht filelist so that we can compare to the server dht
    def fileList(self):
        path = os.getcwd() + "\\Server Test Files"
        x =  P2P.shittydht.populateDHT(path)
        return x

    """
    Sending info to the clients and closing the connection if the client has left.
    @param connection The connection server is connected to.
    @param a (ip address, port) of the system connected.
    """
    def handler(self, connection, a):
        try:
            while True:
                # server recieves the message
                # socket.recv will read at most BYTE_SIZE bytes, blocking if no data is waiting to be read
                clientList = pickle.loads(connection.recv(BYTE_SIZE))
               
                # start comparisons
                self.comparedht(clientList)
                        
        except (KeyboardInterrupt, SystemExit) as e:
            print("INTERRUPT: INSIDE OF HANDLER")
            sys.exit()

    """
    Disconnect a peer.
    @param connection The connection server is connected to.
    @param a (ip address, port) of the system connected.
    """
    def disconnect(self, connection, a):
        # remove the connection from the list of connections
        self.connections.remove(connection)
        # remove ip address, port from the list of peers
        self.peers.remove(a)
        # close the connection
        connection.close()
        # send a list of peers to all the peers that are connected to the server
        self.sendPeersList()
        # output which peer got disconnected
        print("{}, disconnected".format(a))


    """
    Run the server and create a different thread to handle each client
    """
    def run(self):
        # constantly listen for connections
        try:
            # socket.accept() accept a connection. the return value is a pair (conn, address)
            connection, a = self.s.accept()

            # append the address to the list of peers
            self.peers.append(a)
            # output the list of peers
            #print("Peers are: {}".format(self.peers) )
            # send a list of peers to all the peers that are connected to the server
            #self.sendPeersList()

            # append connection to the list of connections
            self.connections.append(connection)
            # output the address of the new connection
            print("{}, has connected to the server".format(a))

            # create a thread for a connection
            connThread = threading.Thread(target=self.handler, args=(connection, a))
            #connThread.daemon = True
            connThread.start()
            connThread.join()
            

        except (KeyboardInterrupt, SystemExit) as e:
            print("INTERRUPT: INSIDE OF RUN")
            sys.exit()

    """
    send a list of peers to all the peers that are connected to the server
    """
    def sendPeersList(self):
        peerList = ""
        for peer in self.peers:
            peerList = peerList + str(peer[0]) + ","

        for connection in self.connections:
            # add a byte '\x11' at the begning of the our byte to can differentiate if we recieved a message for a list of peers
            data = PEER_BYTE_DIFFERENTIATOR + bytes(peerList, 'utf-8')
            connection.send(data)
