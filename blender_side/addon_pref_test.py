bl_info = {
    "name": "Cascadeur to Blender",
    "author": "Aron Nemeth",
    "version": (0, 1),
    "blender": (3, 5, 0),
    "location": "View3D > Panels > csc2blend",
    "description": "Helps you import animations from Cascadeur",
    "doc_url": "https://github.com/arcsikex/cacs-to-blender",
    "tracker_url": "https://github.com/arcsikex/cacs-to-blender/issues",
    "category": "Animation",
}

import bpy
import os
import platform
import socket
import select
import subprocess


def get_default_casc_path():
    default_csc_path = {
        "Windows": r"C:\Program Files\Cascadeur\cascadeur.exe",
    }
    return default_csc_path.get(platform.system(), None)


def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path) and os.path.isfile(file_path)


def delete_file(file_path):
    if file_exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")


def execut_csc_command(csc_path: str, command: str) -> None:
    subprocess.call([csc_path, command])


class MyAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    csc_exe_path: bpy.props.StringProperty(
        name="File Path",
        subtype="FILE_PATH",
        default=get_default_casc_path() if file_exists(get_default_casc_path()) else "",
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Cascadeur Executable path:")
        layout.prop(self, "csc_exe_path")


class StartServerOperator(bpy.types.Operator):
    """Start Socket Server"""

    bl_idname = "object.start_server"
    bl_label = "Start Server"

    _server_socket = None
    _socket_list = []
    _buffer_size = 1024

    def modal(self, context, event):
        if event.type == "ESC":
            self._server_socket.close()
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
                    exported_file = data.decode()
                    print("Received:", exported_file)
                    sock.sendall(b"File path recieved by Blender")
                    delete_file(exported_file)
                    return {"FINISHED"}
                else:
                    sock.close()
                    self._socket_list.remove(sock)

        return {"RUNNING_MODAL"}

    def execute(self, context):
        # Send command to Cascadeur
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        addon_prefs.csc_exe_path
        execut_csc_command(
            addon_prefs.csc_exe_path, "commands.quick_export.temp_export.py"
        )

        # Start Server
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(("localhost", 12345))
        self._server_socket.listen(5)
        self._socket_list = [self._server_socket]  # reset the list
        print("Socket server started")

        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def cancel(self, context):
        self._server_socket.close()
        print("Socket server stopped")


def register():
    bpy.utils.register_class(MyAddonPreferences)
    bpy.utils.register_class(StartServerOperator)


def unregister():
    bpy.utils.unregister_class(MyAddonPreferences)
    bpy.utils.unregister_class(StartServerOperator)
