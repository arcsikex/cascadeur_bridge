import bpy

from .addon_properties import get_csc_export_settings
from ..utils import file_handling
from ..utils.server_socket import ServerSocket
from ..utils.csc_handling import CascadeurHandler


def import_fbx(file_path: str) -> list:
    bpy.ops.import_scene.fbx(
        filepath=file_path,
        # Transform
        global_scale=1.0,
        bake_space_transform=False,  # Apply Transform
        use_manual_orientation=False,
        axis_forward="-Z",
        axis_up="Y",
        # Animation
        use_anim=True,
        anim_offset=1.0,
        # Armature
        ignore_leaf_bones=True,
        force_connect_children=False,
        automatic_bone_orientation=False,
        primary_bone_axis="Y",
        secondary_bone_axis="X",
        use_prepost_rot=False,
    )
    # Return the list of imported objects
    return bpy.context.selected_objects


def export_fbx(file_path: str) -> None:
    bpy.ops.export_scene.fbx(
        filepath=file_path,
        # Include
        use_selection=True,
        use_visible=False,
        use_active_collection=False,
        object_types={"EMPTY", "CAMERA", "LIGHT", "ARMATURE", "MESH", "OTHER"},
        # Transform
        global_scale=1.0,
        axis_forward="-Z",
        axis_up="Y",
        bake_space_transform=False,
        # Armature
        primary_bone_axis="Y",
        secondary_bone_axis="X",
        use_armature_deform_only=True,
        add_leaf_bones=False,
        # Animation
        bake_anim=True,
        bake_anim_use_nla_strips=True,
        bake_anim_use_all_actions=True,
    )


def get_actions_from_objects(selected_objects: list) -> list:
    actions = []
    for obj in selected_objects:
        if obj.type == "ARMATURE":
            actions.append(obj.animation_data.action)
    return actions


def delete_objects(objects: list) -> None:
    for obj in objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    # Update the scene to reflect the changes
    bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)


def apply_action(armature, action) -> None:
    action.name = "cascadeur_action"
    if not hasattr(armature.animation_data, "action"):
        armature.animation_data_create()
    armature.animation_data.action = action


class CBB_OT_export_blender_fbx(bpy.types.Operator):
    """Exports the selected objects and imports them to Cascadeur"""

    bl_idname = "cbb.export_blender_fbx"
    bl_label = "Export to Cascadeur"

    server_socket = None
    file_path = None

    def __del__(self):
        self.server_socket.close()

    def modal(self, context, event):
        if event.type == "ESC":
            return {"CANCELLED"}

        self.server_socket.run()

        if self.server_socket.client_socket:
            self.server_socket.send_message(self.file_path)
            response = self.server_socket.receive_message()
            if response == "SUCCESS":
                print("File successfully imported to Cascadeur.")
                file_handling.delete_file(self.file_path)
                self.report({"INFO"}, "Finished")
                return {"FINISHED"}
            else:
                return {"CANCELLED"}

        return {"PASS_THROUGH"}

    def execute(self, context):
        self.server_socket = ServerSocket()

        self.file_path = file_handling.get_export_path()
        export_fbx(self.file_path)
        CascadeurHandler().execute_csc_command("commands.externals.temp_importer")
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


class CBB_OT_import_cascadeur_fbx(bpy.types.Operator):
    """Imports the currently opened Cascadeur scene"""

    bl_idname = "cbb.import_cascadeur_fbx"
    bl_label = "Import Cascadeur Scene"

    server_socket = None

    def __del__(self):
        self.server_socket.close()

    def modal(self, context, event):
        if event.type == "ESC":
            return {"CANCELLED"}

        self.server_socket.run()

        if self.server_socket.client_socket:
            self.server_socket.send_message(get_csc_export_settings())
            data = self.server_socket.receive_message()
            if data:
                print(str(data))
                file_handling.wait_for_file(data)
                import_fbx(data)
                file_handling.delete_file(data)
                self.report({"INFO"}, "Finished")
                return {"FINISHED"}

        return {"PASS_THROUGH"}

    def execute(self, context):
        self.server_socket = ServerSocket()
        CascadeurHandler().execute_csc_command("commands.externals.temp_exporter")
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

    def __del__(self):
        self.server_socket.close()

    def modal(self, context, event):
        if event.type == "ESC":
            return {"CANCELLED"}

        self.server_socket.run()

        if self.server_socket.client_socket:
            self.server_socket.send_message(get_csc_export_settings())
            data = self.server_socket.receive_message()
            if data:
                print(str(data))
                file_handling.wait_for_file(data)
                imported_objects = import_fbx(data)
                file_handling.delete_file(data)
                actions = get_actions_from_objects(imported_objects)
                apply_action(self.ao, actions[0])
                delete_objects(imported_objects)
                self.report({"INFO"}, "Finished")
                return {"FINISHED"}

        return {"PASS_THROUGH"}

    def execute(self, context):
        self.ao = bpy.context.active_object
        self.server_socket = ServerSocket()
        CascadeurHandler().execute_csc_command("commands.externals.temp_exporter")
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
