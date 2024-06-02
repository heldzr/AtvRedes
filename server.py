import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except Exception:
                client.close()
                if client in clients:
                    clients.remove(client)

def handle_client(conn, addr):
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                else:
                    print(f"[{addr}] {msg}")
                    broadcast(msg.encode(FORMAT), conn)
        except (ConnectionResetError, ValueError):
            connected = False

    conn.close()
    if conn in clients:
        clients.remove(conn)
        print(f"[DESCONECTADO] {addr} desconectado.")
        print(f"[CONEXÕES ATIVAS] {len(clients)}")

def start():
    server.listen()
    print(f"[OUVINDO] Servidor ouvindo em {SERVER}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXÕES ATIVAS] {len(clients)}")

print("[INICIANDO] Servidor está iniciando...")
start()
