import socket
import select
import json
from typing import Any
from . import config_handling


class ServerSocket:
    _header = 64
    _host = "localhost"
    _format = "utf-8"

    def __init__(self):
        self._port = config_handling.get_config_parameter(
            "Addon Settings", "port", fallback=53145, data_type=int
        )
        print(f"[CSC Bridge] Attempting to create socket on {self._host}:{self._port}")
        try:
            localhost_ip = socket.gethostbyname("localhost")
            print(f"[CSC Bridge] 'localhost' resolves to IP: {localhost_ip}")
            if localhost_ip != "127.0.0.1":
                print(
                    f"[CSC Bridge] WARNING: 'localhost' is not resolving to the standard 127.0.0.1 address"
                )
        except socket.gaierror:
            print(
                f"[CSC Bridge] ERROR: Cannot resolve 'localhost' to an IP address. This may be the source of the binding problem"
            )
        # Check if port is already in use BEFORE trying to bind
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(1)
            result = test_socket.connect_ex((self._host, self._port))
            test_socket.close()
            if result == 0:
                print(
                    f"[CSC Bridge] ERROR: Port {self._port} is already in use by another application"
                )
                print(
                    f"[CSC Bridge] Please select a different port in the addon settings"
                )
                raise socket.error(f"Port {self._port} is already in use")
        except socket.error as test_error:
            print(
                f"[CSC Bridge] NOTE: Port availability test encountered: {test_error}"
            )

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self._host, self._port))
        self.sock.listen(1)
        self.client_socket = None
        print(f"[CSC Bridge] Server listening on {self._host}:{self._port}")

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
            print("[CSC Bridge] ", message)
            self.client_socket.send(message)
        except Exception as e:
            print(f"[CSC Bridge] Couldn't send message. Error: {e}")
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
            print(f"[CSC Bridge] Couldn't recieve message. Error: {e}")
            return False
        message = json.loads(message)
        print("[CSC Bridge] ", message)
        return message

    def run(self) -> None:
        """
        Start socket and wait for connection.
        """
        ready, _, _ = select.select([self.sock], [], [], 0)
        if ready:
            self.client_socket, client_address = self.sock.accept()
            print(f"[CSC Bridge] Connection from {client_address}")

    def close(self) -> None:
        """
        Closing the socket.
        """
        try:
            self.sock.close()
        except:
            pass
