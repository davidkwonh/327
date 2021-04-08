import socket

s = socket.socket()
host = input(str("Please enter the hose address of sender: "))
port = 8080
s.connect((host, port))
print("Connected...")