import os
import socket

def test():
    print(socket.gethostname())
    print()

    devices = []

    for device in os.popen('arp -a'): 
        print(device)

        
def main():
    test()

if __name__ == "__main__":
    main()
