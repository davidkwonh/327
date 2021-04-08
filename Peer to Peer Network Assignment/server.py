import socket

s = socket.socket()
host = socket.gethostname()
port = 8080
s.bind((host, port))
s.listen(1)
print(host)
print("Waiting for any incoming connections...")
conn, addr = s.accept()
print(addr, "Has connected to the server")