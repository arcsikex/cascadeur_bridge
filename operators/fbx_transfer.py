import bpy
import os

from ..utils import file_handling
from ..utils.server_socket import ServerSocket
from ..utils.csc_handling import CascadeurHandler


def import_fbx(file_path: str) -> list:
    # Set import settings
    bpy.ops.import_scene.fbx(
        filepath=file_path,
        use_anim=True,
        use_image_search=True,
        force_connect_children=False,
        automatic_bone_orientation=False,
        use_prepost_rot=False,
        ignore_leaf_bones=True,
        primary_bone_axis="Y",
        secondary_bone_axis="X",
        global_scale=1.0,
        use_manual_orientation=False,
        axis_forward="-Z",
        axis_up="Y",
    )
    # Return the list of imported objects
    return bpy.context.selected_objects


def export_fbx(file_path: str) -> None:
    bpy.ops.export_scene.fbx(
        filepath=file_path,
        use_selection=True,
        add_leaf_bones=False,
        # primary_bone_axis="Y",
        # axis_up="Z",
        # axis_forward="-Y",
        bake_anim=True,
    )


def get_actions_from_objects(selected_objects: list):
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


class CBB_OT_export_blender_fbx(bpy.types.Operator):
    """Exports the selected objects and imports them to Cascadeur"""

    bl_idname = "cbb.export_blender_fbx"
    bl_label = "Export to Cascadeur"

    server_socket = None
    file_path = None

    def modal(self, context, event):
        if event.type == "ESC":
            self.server_socket.close()
            return {"CANCELLED"}

        self.server_socket.run()

        if self.server_socket.client_socket:
            self.server_socket.send_message(self.file_path)
            response = self.server_socket.receive_message()
            if response == "SUCCESS":
                print("File successfully imported to Cascadeur.")
                self.server_socket.close()
                file_handling.delete_file(self.file_path)
                return {"FINISHED"}
            else:
                self.server_socket.close()
                return {"CANCELLED"}

        return {"PASS_THROUGH"}

    def execute(self, context):
        self.server_socket = ServerSocket()

        self.file_path = file_handling.get_export_path()
        export_fbx(self.file_path)
        CascadeurHandler().execute_csc_command("commands.externals.temp_importer.py")
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


class CBB_OT_import_cascadeur_fbx(bpy.types.Operator):
    """Imports the currently opened Cascadeur scene"""

    bl_idname = "cbb.import_cascadeur_fbx"
    bl_label = "Import Cascadeur Scene"

    server_socket = None

    def modal(self, context, event):
        if event.type == "ESC":
            self.server_socket.close()
            return {"CANCELLED"}

        self.server_socket.run()

        if self.server_socket.client_socket:
            data = self.server_socket.receive_message()
            if data:
                print(str(data))
                file_handling.wait_for_file(data)
                import_fbx(data)
                file_handling.delete_file(data)
                self.server_socket.close()
                return {"FINISHED"}

        return {"PASS_THROUGH"}

    def execute(self, context):
        self.server_socket = ServerSocket()
        CascadeurHandler().execute_csc_command("commands.externals.temp_exporter.py")
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


class CBB_OT_import_action_to_selected(bpy.types.Operator):
    """Imports the action from Cascadeur and apply to selected armature"""

    bl_idname = "cbb.import_cascadeur_action"
    bl_label = "Import Cascadeur Action"

    ao = None

    @classmethod
    def poll(cls, context):
        return (
            context.active_object
            and context.selected_objects
            and context.active_object.type == "ARMATURE"
        )

    def modal(self, context, event):
        if event.type == "ESC":
            self.server_socket.close()
            return {"CANCELLED"}

        self.server_socket.run()

        if self.server_socket.client_socket:
            data = self.server_socket.receive_message()
            if data:
                print(str(data))
                file_handling.wait_for_file(data)
                imported_objects = import_fbx(data)
                file_handling.delete_file(data)
                actions = get_actions_from_objects(imported_objects)
                apply_action(self.ao, actions)
                delete_objects(imported_objects)
                self.server_socket.close()
                return {"FINISHED"}

        return {"PASS_THROUGH"}

    def execute(self, context):
        self.ao = bpy.context.active_object
        self.server_socket = ServerSocket()
        CascadeurHandler().execute_csc_command("commands.externals.temp_exporter.py")
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


# Should be moved to a different place
class CBB_OT_start_cascadeur(bpy.types.Operator):
    """Start Cascadeur"""

    bl_idname = "cbb.start_cascadeur"
    bl_label = "Start Cascadeur"

    @classmethod
    def poll(cls, context):
        return CascadeurHandler().is_csc_exe_path_valid

    def execute(self, context):
        CascadeurHandler().start_cascadeur()
        return {"FINISHED"}


ADDON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class CBB_OT_install_required_files(bpy.types.Operator):
    """Copy the necessary DLLs and python script to Cascadeurs folder"""

    bl_idname = "cbb.install_required_files"
    bl_label = "Install Required Files"

    @classmethod
    def poll(cls, context):
        return CascadeurHandler().is_csc_exe_path_valid

    def execute(self, context):
        ch = CascadeurHandler()
        # Copy commands
        commands_source = os.path.join(ADDON_PATH, "csc_files", "externals")
        commands_path = os.path.join(ch.commands_path, "externals")
        result = file_handling.copy_files(
            commands_source, commands_path, ch.required_scripts
        )
        if not result:
            self.report(
                {"ERROR"}, "You don't have permission to copy the files for Cascadeur"
            )
            self.report({"INFO"}, "Restart Blender as Admin and try again")
            return {"CANCELLED"}

        # Copy DLLs
        dlls_source = os.path.join(ADDON_PATH, "csc_files")
        dlls_path = os.path.join(ch.csc_dir, "python", "DLLs")
        result = file_handling.copy_files(
            dlls_source, dlls_path, ch.required_dlls, overwrite=False
        )
        if not result:
            self.report(
                {"ERROR"}, "You don't have permission to copy the files for Cascadeur"
            )
            self.report({"INFO"}, "Restart Blender as Admin and try again")
            return {"CANCELLED"}
        self.report({"INFO"}, "All necessary files have been successfully copied")
        return {"FINISHED"}
