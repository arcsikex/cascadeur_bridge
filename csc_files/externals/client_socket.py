import socket
import json
from typing import Any

import csc


class ClientSocket:
    _header = 64
    _host = "localhost"
    _port = 1234
    _format = "utf-8"

    scene = csc.app.get_application().current_scene().domain_scene()

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self._host, self._port))

    def send_message(self, message: Any) -> bool:
        """
        Message to be sent to Cascadeur json serialized.
        First the message length will be sent, then the actual message.

        :param Any message: Message to be sent
        :return bool: False in case of an exception, otherwise True
        """
        message = json.dumps(message, ensure_ascii=False)
        message = message.encode(self._format)
        # Sending the lenght of the message padded to be the size of _header
        msg_length = str(len(message)).encode(self._format)
        msg_length += b" " * (self._header - len(msg_length))
        try:
            # Sending the header
            self.client_socket.send(msg_length)
            # Sending the message
            self.client_socket.send(message)
        except Exception as e:
            self.scene.error(f"Couldn't send message. Error: {e}")
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
            self.scene.error(f"Couldn't recieve message. Error: {e}")
            return False
        message = json.loads(message)
        return message

    def close(self) -> None:
        """
        Closing the socket.
        """
        try:
            self.client_socket.close()
        except:
            pass
