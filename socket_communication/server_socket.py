import socket
import json


class ServerSocket:
    _header = 64
    _host = "localhost"
    _port = 53169
    _format = "utf-8"

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self._host, self._port))
        self.sock.listen(1)
        self.client_socket = None
        print(f"Server listening on {self._host}:{self._port}")

    def send_message(self, message):
        message = json.dumps(message, ensure_ascii=False)
        message = message.encode(self._format)
        msg_length = str(len(message)).encode(self._format)
        msg_length += b" " * (self._header - len(msg_length))
        # Sending the message
        self.client_socket.send(msg_length)
        self.client_socket.send(message)

    def receive_message(self):
        # Recieve the messagge
        msg_length = self.client_socket.recv(self._header).decode(self._format)
        msg_length = int(msg_length)
        message = self.client_socket.recv(msg_length).decode(self._format)
        message = json.loads(message)
        return message

    def run(self):
        self.client_socket, client_address = self.sock.accept()
        print(f"Connection from {client_address}")

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    fbx_settings = {"up_axis": "Y", "mode": "binary"}
    s = ServerSocket()
    while True:
        s.run()
        if s.client_socket:
            print("Client connected")
            print(s.receive_message())
            s.send_message(fbx_settings)
            s.close()
            break
