import bpy

import socket
import select

global recieved_data
recieved_data = None


class CT_OT_start_server(bpy.types.Operator):
    """Start Socket Server"""

    bl_idname = "ct.start_server"
    bl_label = "Get Animation From Cascadeur"

    _server_socket = None
    _socket_list = []
    _buffer_size = 1024
    _active_object = None

    def modal(self, context, event):
        if event.type == "ESC":
            self._server_socket.close()
            self._server_socket = None
            return {"CANCELLED"}

        readable, _, _ = select.select(self._socket_list, [], [], 0.1)
        for sock in readable:
            if sock == self._server_socket:
                client_socket, address = self._server_socket.accept()
                self._socket_list.append(client_socket)
                print("Connection from", address)
            else:
                data = sock.recv(self._buffer_size)
                if data:
                    global recieved_data
                    recieved_data = data.decode()
                    print("Received:", recieved_data)
                    sock.sendall(b"File path recieved by Blender")
                    return {"FINISHED"}
                else:
                    sock.close()
                    self._socket_list.remove(sock)
                    self._server_socket = None

        return {"RUNNING_MODAL"}

    def execute(self, context):
        # Start Server
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(("localhost", 12345))
        self._server_socket.listen(5)
        self._socket_list = [self._server_socket]
        print("Socket server started")

        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def cancel(self, context):
        self._server_socket.close()
        self._server_socket = None
        print("Socket server stopped")
