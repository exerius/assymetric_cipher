import socket
import encoding
from threading import Thread
from random import choice

def IO(port):
    sock = socket.socket()
    sock.bind((HOST, int(port)))
    sock.listen(1)
    conn, addr = sock.accept()
    while True:
        msg = conn.recv(1024).decode()
        msg_decr = encoding.decrypt(msg, K)
        print(f"Сообщение: {msg}")
        print(f"Расшифрованное сообщение: {msg_decr}")
        conn.send(encoding.encrypt(msg_decr, K).encode())
        if msg_decr == "exit":
            break
    conn.close()
    chosen.remove(port)

HOST = '127.0.0.1'
PORT = 8080
threads = []
pool = [str(i) for i in range(80, 90)]
chosen = []
while True:
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    p, g, a, A = encoding.gen_key_server()
    print(f"Тайный ключ:{a}\nПубличный ключ: {p}, {g}, {A}")
    encoding.send_key((p, g, A), conn)
    K = encoding.get_K_server(a, p, conn)
    print(f"Общий ключ: {K}")
    if K != "CONNECTION_ERROR":
        if len(pool) == len(chosen):
            sock.send(encoding.encrypt("CONNECTION_ERROR", K))
        else:
            port_number = choice(pool)
            while port_number in chosen:
                port_number = choice(pool)
            chosen.append(port_number)

        conn.send(encoding.encrypt(port_number, K).encode())
        sock.close()
        print(f"Общение происходит на порту: {port_number}")
        threads.append(Thread(target=IO, args=[port_number]))
        threads[len(threads)-1].start()
