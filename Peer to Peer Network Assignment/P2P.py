import os
import sys
import socket
import time
from random import randint
from client import *
from server import *

directpath = os.getcwd() + "\\Test Files"
# hard coded path to test directory 
#directpath = "C:\\Users\\castr\\OneDrive - CSULB\\CECS 327\\Term Project\\Peer to Peer Network Assignment\\Test Files"
# using a test file for now 
prevdir = directpath + "/read_file.txt"
# new file to write to
newdir = directpath + "/new_file.txt"


#hashmap for transactions between servers and clients
class shittydht:
    dht = {}

    def populateDHT():
        dictionary = {}

        for filename in os.listdir(directpath):
            dir = directpath + '/' + filename
            with open(dir, 'r') as file:
                read_data = file.read()
                dictionary[filename] = read_data.encode("utf-8")
        return dictionary


class ip:
    # make ourself the default peer
    address = ['127.0.0.1']

#sending the file in as an encrypted utf-8 hash
#before sending the hash, the dht is populated with a key of the file name and the value of the encrypted hash
def prepfile(dir=prevdir):
    read_data = None
    with open(dir, 'r') as file:
        read_data = file.read()
        shittydht.dht[file].append(read_data.encode("utf-8"))
    return read_data.encode("utf-8")

#this receives the encrypted file, decrypts it, then saves it to specified local directory that is hard coded as a variable
def makefile(encrypted_file):
    encrypted_file = encrypted_file.decode("utf-8")
    print("Writing to file")
    with open(newdir, 'w') as file:
        file.write(encrypted_file)
    return True

def compare():
    with open(dir, 'r') as file:
        read_data = file.read()



def main():
    # populate initial DHT before deciding if client or server
    fileList = shittydht.populateDHT()

    #targetfile = prepfile()
    #makefile(targetfile)
    #msg = prepfile()

    while True:
        try:
            print("Establishing Connection")
            # sleep a random time between 1 - 10 seconds
            #time.sleep(randint(1, 10))
            time.sleep(1)
            for ipaddy in ip.address:
                print(ipaddy)
                try:
                    client = Client(ipaddy, fileList)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

                # become the server
                try:
                    server = Server(fileList)
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
