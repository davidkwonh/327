import socket
import threading
import sys
import time
import P2P
import pickle # to send dictionary over 
import os

BYTE_SIZE = 1024
HEADERSIZE = 10
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
PEER_BYTE_DIFFERENTIATOR = b'\x11' 
REQUEST_STRING = "req"

class Client:
    # Constructor for client
    def __init__(self, addr):
        try:
            # AF_INET is a pair (host, port) where host is hostname in domain and port is port number being used
            # SOCK_STREAM is default type for socket which is pretty much TCP. Keeps connection until terminated. 
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # (level, optname, value)
            # level: SOL_SOCKET meaning manipulate options at the socket API level
            # optname: SO_REUSEADDR meaning to reuse socket address in case of client closing 
            # value: integer representing buffer 
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.dht = self.fileList()

            # Connect to remote socket (addr) using specified port number
            self.s.connect((addr, PORT))

            self.previous_data = None

            # output if the server is running
            print("Client Running")

            self.run()

        except KeyboardInterrupt as e:
            print("INTERRUPT INSIDE OF INIT")
            sys.exit()
        
        """
        #Unecessary code for now
        # Constructor for initial thread where target is send message function for client
        # Daemon: needs to be set to True before start() called to avoid runtime error
        # Daemon thread will run without blocking main thread
        # thread activity started with start()
        initial = threading.Thread(target = self.send_message)
        initial.daemon = True
        initial.start()

        # Loop to receive data using a thread for receive_message()
        while True:
            receive = threading.Thread(target = self.receive_message)
            receive.start()
            receive.join()

            # 
            data = self.receive_message()

            if not data:
                # error occured with sending data
                print("ERROR: Data transfer was unsuccessful.")
            
            elif data[0:1] == b'\x11':
                print("Got peers.")
                self.update_peers(data[1:])
        """

    # a function to return a dht filelist so that we can compare to the server dht
    def fileList(self):
        path = os.getcwd() + "\\Client Test Files"
        x =  P2P.shittydht.populateDHT(path)
        return x

    def run(self):
        self.initialConnection()
        try:
            i_thread = threading.Thread(target=self.waitForCompare)
            i_thread.start()
            i_thread.join()

            time.sleep(1)
        
        except:
            print("Failed compare")

    def waitForCompare(self):
        while True:
            time.sleep(2)
            code = self.s.recv(BYTE_SIZE).decode('utf-8')

            if code == "s":
                # need to send file over
                fileName = self.s.recv(BYTE_SIZE).decode('utf-8')
                msg = self.dht[fileName][0]
                self.s.send(msg)

            elif code == "r":
                fileName = self.s.recv(BYTE_SIZE).decode('utf-8')
                # will receive file
                fileContent = self.s.recv(BYTE_SIZE).decode('utf-8')

                # create a new file in case 
                if self.previous_data != fileContent: 
                    # Test to see if this works properly
                    P2P.makefile(fileName, fileContent, "Client Test Files")
                    self.previous_data = data

            elif code == "q":
                # no more data, we can leave
                break
        
        self.dht()
            
    
    def initialConnection(self):
        # Send over DHT 
        dict_DHT = pickle.dumps(self.fileList())

        self.s.sendall(dict_DHT)
        
    """
    def send_message(self, msg):
        #TODO Finish up function
        try:
            print("Sending...")
            # encode message with UTF-8 codec and send 
            #self.s.send(REQUEST_STRING.encode('utf-8'))
            self.s.send(msg.encode('utf-8'))

        except KeyboardInterrupt as e:
            self.send_disconnect_signal()
            return


    def receive_message(self):
        #TODO NEED TO TEST
        print("Receiving...")
        data = self.s.recv(BYTE_SIZE)

        # test to see if we have data
        print(data.decode("utf-8"))
        print("\nRecieved message on the client side is:")

        # create a new file in case 
        if self.previous_data != data:
            # TODO 
            # Test to see if this works properly
            P2P.makefile(data)
            self.previous_data = data
        
        return data
    """

    def update_peers(self, peers):
        # -1 to remove the last value (None)
        p2p.peers = str(peers, "utf-8").split(',')[:-1]

    def create_file(data):
        # decode(encoding)
        # decoding the string with UTF-8 codec
        data = data.decode("utf-8")
        print("Writing to file")

        # opening new file and writing data
        with open(new_file_path, 'w') as file:
            file.write(data)

        return True


    def send_disconnect_signal(self):
        # Print message and send a signal to the server
        print("Disconnected from server")
        self.s.send("q".encode('utf-8'))
        sys.exit()
