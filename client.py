import socket
import encoding
HOST = '127.0.0.1'
PORT = 8080
sock = socket.socket()
sock.connect((HOST, PORT))
b = encoding.gen_key_client()
K = encoding.get_K_client(b, sock)
try:
    port_number = int(encoding.decrypt(sock.recv(1024).decode(), K))
except ValueError:
    port_number = "CONNECTION_ERROR"
if port_number != "CONNECTION_ERROR":
    sock.close()
    sock = socket.socket()
    sock.connect((HOST, port_number))
    while True:
        sock.send(encoding.encrypt(input("Введите сообщение\n"), K).encode())
        msg = sock.recv(1024).decode()
        if encoding.decrypt(msg, K) != "exit":
            print(f"Сообщение: {msg}\nРасшифрованное сообщение: {encoding.decrypt(msg, K)}")
        else:
            break
    sock.close()
else:
    print("Неправильный ключ")
