# For testing purpose
import socket
import time


def send_file_path(message):
    server_address = ("localhost", 12345)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    attempts = 0
    while True:
        try:
            client_socket.connect(server_address)
            break
        except ConnectionRefusedError:
            if attempts < 10:
                attempts += 1
                time.sleep(0.1)
            else:
                raise
    client_socket.sendall(message.encode())
    response = client_socket.recv(1024)
    print(response.decode())
    client_socket.close()


import tempfile
import os


def get_export_path():
    temp_dir = tempfile.gettempdir()
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return os.path.join(temp_dir, f"temp_export_{current_time}")


send_file_path(get_export_path())
