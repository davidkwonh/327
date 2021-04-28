import os
import socket
from client import *
from server import *

directpath = os.getcwd()
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
    encrypted_file = data.decode("utf-8")
    print("Writing to file")
    with open(newdir, 'w') as file:
        file.write(encrypted_file)
    return True


def main():
    targetfile = prepfile()
    makefile(targetfile)

    msg = fileIO.convert_to_bytes()
    while True:
        try:
            print("Establishing Connection")
            # sleep a random time between 1 -5 seconds
            time.sleep(randint(RAND_TIME_START, RAND_TIME_END))
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

def main():
    test()

if __name__ == "__main__":
    main()
