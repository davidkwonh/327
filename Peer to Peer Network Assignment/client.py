import socket
import threading
import sys
import time
import P2P

BYTE_SIZE = 1024
HOST = '127.0.0.1'
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

            # Connect to remote socket (addr) using specified port number
            self.s.connect((addr, PORT))

            self.previous_data = None


            # output if the server is running
            print("-" * 3 + "Client Running"+ "-" * 3)

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
        return shittydht.populateDHT()

    def run(self):
        print("This will be where interaction with server happens")

    def send_message(self):
        #TODO Finish up function
        try:
            print("Sending...")
            # encode message with UTF-8 codec and send 
            self.s.send(REQUEST_STRING.encode('utf-8'))
            self.s.send(fileList)

        except KeyboardInterrupt as e:
            self.send_disconnect_signal()
            return

    def receive_message(self):
        #TODO NEED TO TEST
        print("Recieving...")
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