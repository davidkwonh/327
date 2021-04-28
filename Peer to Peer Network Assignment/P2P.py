import os
import socket
from client import *
from server import *

directpath = os.getcwd()
prevdir = directpath + "/read_file.txt"
newdir = directpath + "/new_file.txt"

def prepfile(dir=prevdir):
    read_data = None
    with open(dir, 'r') as file:
        read_data = file.read()
    return read_data.encode("utf-8")

def makefile(encrypted_file):
    encrypted_file = data.decode("utf-8")
    print("Writing to file")
    with open(newdir, 'w') as file:
        file.write(encrypted_file)
    return True


def main():
    targetfile = prepfile()
    makefile(targetfile)

def test():
    print(socket.gethostname())
    devices = []
    for device in os.popen('arp -a'): 
        print(device)

def main():
    test()

if __name__ == "__main__":
    main()
