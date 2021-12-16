from random import randint
import pickle
import socket


def encrypt(message, cypher):
    return "".join(list(map(lambda x: chr(ord(x) ^ cypher), list(message))))


def decrypt(message, cypher):
    return encrypt(message, cypher)


def gen_key_server():
    try:
        with open("server_private_key.txt", "r") as file:
            a = int(file.read())
    except OSError:
        a = randint(1, 10000)
    try:
        with open("server_public_key.txt", "r") as file:
            line = list(map(int, list(file.read())))
            p = line[0]
            g = line[1]
    except OSError:
        p = randint(1, 10000)
        g = randint(1, 10000)
    return p, g, a, g ** a % p


def gen_key_client():
    try:
        with open("client_private_key.txt", "r") as file:
            b = int(file.read())
    except OSError:
        b = randint(1, 10000)
    return b


def get_K_server(a, p, conn):
    b = pickle.loads(conn.recv(1024))
    allowed = []
    with open("allowed_keys.txt", "r") as file:
        for i in file:
            allowed.append(int(i))
    if b not in allowed:
        conn.close()
        return "CONNECTION_ERROR"
    else:
        return b ** a % p


def get_K_client(b, sock):
    p, g, a = pickle.loads(sock.recv(1024))
    sock.send(pickle.dumps(g ** b))
    return a ** b % p


def send_key(key, sock):
    sock.send(pickle.dumps(key))
