import socket
import pickle
from random import randint
HOST = '127.0.0.1'
PORT = 80
sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen()
conn, addr = sock.accept()
print(pickle.loads(conn.recv(1024)))
