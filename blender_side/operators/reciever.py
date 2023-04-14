import bpy

import socket
import select

from ..utils import file_handling, csc_handling


def import_fbx(file_path: str) -> list:
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
    return bpy.context.selected_objects


def get_action_from_objects(selected_objects: list):
    actions = []
    for obj in selected_objects:
        if obj.type == "ARMATURE":
            actions.append(obj.animation_data.action)
    return actions


def delete_objects(objects):
    for obj in objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    # Update the scene to reflect the changes
    bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)


def apply_action(armature, actions: list):
    if len(actions) == 1:
        actions[0].name = "cascadeur_action"
        if not hasattr(armature.animation_data, "action"):
            armature.animation_data_create()
        armature.animation_data.action = actions[0]


class CT_OT_get_animamtion_from_cascadeur(bpy.types.Operator):
    """Start Socket Server"""

    bl_idname = "object.start_server"
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
                    exported_file = data.decode()
                    print("Received:", exported_file)
                    sock.sendall(b"File path recieved by Blender")
                    imported_objects = import_fbx(exported_file)
                    actions = get_action_from_objects(imported_objects)
                    apply_action(self._active_object, actions)
                    delete_objects(imported_objects)
                    file_handling.delete_file(exported_file)
                    return {"FINISHED"}
                else:
                    sock.close()
                    self._socket_list.remove(sock)
                    self._server_socket = None

        return {"RUNNING_MODAL"}

    def execute(self, context):
        self._active_object = bpy.context.active_object
        # Send command to Cascadeur
        preferences = context.preferences
        addon_prefs = preferences.addons["blender_side"].preferences
        addon_prefs.csc_exe_path
        csc_handling.execut_csc_command(
            addon_prefs.csc_exe_path, "commands.quick_export.temp_export.py"
        )

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
