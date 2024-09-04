import socket
from concurrent.futures import ThreadPoolExecutor
import threading
import time

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000
MAX_WORKERS = 4  # Number of threads in the pool

def handle_client(client_connection):
    request = client_connection.recv(1024).decode()
    thread_id = threading.get_ident()
    print(f"Request by {thread_id}: {request}")

    time.sleep(3) # Simulate a long process
    response = f"HTTP/1.0 200 OK\n\nHello from {thread_id}!\n"
    client_connection.sendall(response.encode())
    client_connection.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()
print(f"Listening on port {SERVER_PORT} ...")

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    while True:
        client_connection, client_address = server_socket.accept()
        executor.submit(handle_client, client_connection)

server_socket.close()