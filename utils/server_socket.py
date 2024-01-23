import socket
import select
import json
from typing import Any


class ServerSocket:
    _header = 64
    _host = "localhost"
    _port = 53169
    _format = "utf-8"

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self._host, self._port))
        self.sock.listen(1)
        self.client_socket = None
        print(f"Server listening on {self._host}:{self._port}")

    def send_message(self, message: Any) -> bool:
        """
        Message to be sent to Cascadeur json serialized.
        First the message length will be sent, then the actual message.

        :param Any message: Message to be sent
        :return bool: False in case of an exception, otherwise True
        """
        message = json.dumps(message, ensure_ascii=False)
        message = message.encode(self._format)
        msg_length = str(len(message)).encode(self._format)
        msg_length += b" " * (self._header - len(msg_length))
        try:
            # Sending the message
            self.client_socket.send(msg_length)
            print(message)
            self.client_socket.send(message)
        except Exception as e:
            print(f"Couldn't send message. Error: {e}")
            return False
        return True

    def receive_message(self) -> Any:
        """
        Recieve message from Cascadeur decoded from json format.
        First expects the message length, then the actual message.

        :return Any: Decoded message
        """
        try:
            # Recieve the messagge
            msg_length = self.client_socket.recv(self._header).decode(self._format)
            msg_length = int(msg_length)
            message = self.client_socket.recv(msg_length).decode(self._format)
        except Exception as e:
            print(f"Couldn't recieve message. Error: {e}")
            return False
        message = json.loads(message)
        print(message)
        return message

    def run(self) -> None:
        """
        Start socket and wait for connection.
        """
        ready, _, _ = select.select([self.sock], [], [], 0)
        if ready:
            self.client_socket, client_address = self.sock.accept()
            print(f"Connection from {client_address}")

    def close(self) -> None:
        """
        Closing the socket.
        """
        try:
            self.sock.close()
        except:
            pass
