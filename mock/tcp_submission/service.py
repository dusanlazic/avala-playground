import os
import random
import re
import socket
import threading

FLAG_PATTERN = re.compile(os.getenv("FLAG_PATTERN", r"^[A-Z0-9]{31}=$"))


def handle_client(client_socket):
    welcome_message = (
        "Welcome to TEST CTF flag submission! 🏴\nPlease submit one flag per line.\n\n"
    )
    client_socket.sendall(welcome_message.encode("utf-8"))

    try:
        while True:
            flag = client_socket.recv(1024).decode("utf-8").strip()
            if not flag:
                break

            if FLAG_PATTERN.match(flag):
                response_code = "OK" if random.random() < 0.9 else "OLD"
                response = f"{flag} {response_code}\n"
            else:
                response = f"{flag} INV Invalid flag format\n"

            client_socket.sendall(response.encode("utf-8"))

    finally:
        client_socket.close()


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket,)
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server("0.0.0.0", 4444)
