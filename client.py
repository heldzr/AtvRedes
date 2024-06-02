import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    while True:
        try:
            message = client.recv(2048).decode(FORMAT)
            if not message:
                break
            print(message)
        except Exception:
            break
    client.close()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

print("[CONECTADO] Conexão bem-sucedida. Você já pode enviar suas mensagens.")

while True:
    msg = input()
    send(msg)
    if msg == DISCONNECT_MESSAGE:
        break

client.close()
