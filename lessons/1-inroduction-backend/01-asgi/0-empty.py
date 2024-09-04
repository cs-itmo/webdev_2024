import socket
import time

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()
print(f"Listening on port {SERVER_PORT} ...")

while True:
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(1024).decode()
    print(f"Request {request}:\n")
    time.sleep(3) # Simulate a long process

    response = f'HTTP/1.0 200 OK\n\nHello, World!\n'
    client_connection.sendall(response.encode())
    client_connection.close()

server_socket.close()