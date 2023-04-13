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

import socket
import select

from .utils import csc_handling, file_handling


def import_fbx(file_path: str) -> list:
    """Import an FBX file into the current Blender scene."""

    # Set import settings
    bpy.ops.import_scene.fbx(
        filepath=file_path,
        use_anim=True,  # Don't import animations
        use_image_search=True,  # Try to locate missing images
        force_connect_children=False,  # Don't parent objects to armature bones
        automatic_bone_orientation=False,  # Don't automatically orient bones
        use_prepost_rot=False,  # Don't apply pre/post rotation
        ignore_leaf_bones=True,  # Ignore leaf bones (not parented)
        primary_bone_axis="Y",  # Set the primary bone axis to Y
        secondary_bone_axis="X",  # Set the secondary bone axis to X
        global_scale=1.0,
        use_manual_orientation=False,
        axis_forward="-Z",
        axis_up="Y",
    )
    # Return the list of imported objects


class CT_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    _csc_path = csc_handling.get_default_csc_path()

    csc_exe_path: bpy.props.StringProperty(
        name="File Path",
        subtype="FILE_PATH",
        default=_csc_path if file_handling.file_exists(_csc_path) else "",
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Cascadeur Executable path:")
        layout.prop(self, "csc_exe_path")


class CT_OT_get_animamtion_from_cascadeur(bpy.types.Operator):
    """Start Socket Server"""

    bl_idname = "object.start_server"
    bl_label = "Get Animation From Cascadeur"

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
                    import_fbx(exported_file)
                    file_handling.delete_file(exported_file)
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
        csc_handling.execut_csc_command(
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
    bpy.utils.register_class(CT_preferences)
    bpy.utils.register_class(CT_OT_get_animamtion_from_cascadeur)


def unregister():
    bpy.utils.unregister_class(CT_preferences)
    bpy.utils.unregister_class(CT_OT_get_animamtion_from_cascadeur)
