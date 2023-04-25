import socket
import json


class ClientSocket:
    _header = 64
    _host = "localhost"
    _port = 53169
    _format = "utf-8"

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self._host, self._port))

    def send_message(self, message):
        message = json.dumps(message, ensure_ascii=False)
        message = message.encode(self._format)
        # Sending the lenght of the message padded to be the size of _header
        msg_length = str(len(message)).encode(self._format)
        msg_length += b" " * (self._header - len(msg_length))
        self.client_socket.send(msg_length)
        # Sending the message
        self.client_socket.send(message)

    def receive_message(self):
        # Recieve the messagge
        msg_length = self.client_socket.recv(self._header).decode(self._format)
        msg_length = int(msg_length)
        message = self.client_socket.recv(msg_length).decode(self._format)
        message = json.loads(message)
        return message

    def close(self):
        self.client_socket.close()


if __name__ == "__main__":
    paths = r"C:\Windows\System32\cmd.exe"
    c = ClientSocket()
    c.send_message(paths)
    print(c.receive_message())
    c.close()
