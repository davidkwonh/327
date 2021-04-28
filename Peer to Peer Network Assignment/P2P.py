import os
import socket
import time
from random import randint
from client import *
from server import *

#directpath = os.getcwd() + "\\Test Files"
directpath = "C:\\Users\\castr\\OneDrive - csulb\\CECS 327\\P2P\\Test Files"
prevdir = directpath + "/read_file.txt"
newdir = directpath + "/new_file.txt"

class ip:
    # make ourself the default peer
    address = ['127.0.0.1']

def prepfile(dir=prevdir):
    read_data = None
    with open(dir, 'r') as file:
        read_data = file.read()
    return read_data.encode("utf-8")

def makefile(encrypted_file):
    encrypted_file = encrypted_file.decode("utf-8")
    print("Writing to file")
    with open(newdir, 'w') as file:
        file.write(encrypted_file)
    return True


def main():
    targetfile = prepfile()
    makefile(targetfile)

    msg = prepfile()
    while True:
        try:
            print("Establishing Connection")
            # sleep a random time between 1 - 10 seconds
            #time.sleep(randint(1, 10))
            time.sleep(1)
            for ipaddy in ip.address:
                try:
                    client = Client(ipaddy)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

                # become the server
                try:
                    server = Server(msg)
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    pass

        except KeyboardInterrupt as e:
            sys.exit(0)

def test():
    print(socket.gethostname())
    devices = []
    for device in os.popen('arp -a'): 
        print(device)  

if __name__ == "__main__":
    main()
