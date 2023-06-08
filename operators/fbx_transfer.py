import bpy

from .addon_properties import get_csc_export_settings
from ..utils import file_handling
from ..utils.server_socket import ServerSocket
from ..utils.csc_handling import CascadeurHandler
from .. import addon_info

import os


def import_fbx(file_path: str) -> list:
    addon_props = bpy.context.scene.cbb_fbx_settings
    bpy.ops.import_scene.fbx(
        filepath=file_path,
        # Transform
        global_scale=addon_props.cbb_import_global_scale,
        bake_space_transform=addon_props.cbb_import_apply_transform,
        use_manual_orientation=addon_props.cbb_import_manual_orientation,
        axis_forward=addon_props.cbb_import_axis_forward,
        axis_up=addon_props.cbb_import_axis_up,
        # Animation
        use_anim=addon_props.cbb_import_use_anim,
        anim_offset=addon_props.cbb_import_anim_offset,
        # Armature
        ignore_leaf_bones=addon_props.cbb_import_ignore_leaf_bones,
        force_connect_children=addon_props.cbb_import_force_connect_children,
        automatic_bone_orientation=addon_props.cbb_import_automatic_bone_orientation,
        primary_bone_axis=addon_props.cbb_import_primary_bone_axis,
        secondary_bone_axis=addon_props.cbb_import_secondary_bone_axis,
        use_prepost_rot=addon_props.cbb_import_use_prepost_rot,
    )
    # Return the list of imported objects
    return bpy.context.selected_objects


def export_fbx(file_path: str) -> None:
    addon_props = bpy.context.scene.cbb_fbx_settings
    bpy.ops.export_scene.fbx(
        filepath=file_path,
        # Include
        use_selection=addon_props.cbb_export_use_selection,
        object_types=addon_props.cbb_export_object_types,
        # Transform
        global_scale=addon_props.cbb_export_global_scale,
        axis_forward=addon_props.cbb_export_axis_forward,
        axis_up=addon_props.cbb_export_axis_up,
        bake_space_transform=addon_props.cbb_export_apply_transform,
        # Armature
        primary_bone_axis=addon_props.cbb_export_primary_bone_axis,
        secondary_bone_axis=addon_props.cbb_export_secondary_bone_axis,
        use_armature_deform_only=addon_props.cbb_export_deform_only,
        add_leaf_bones=addon_props.cbb_export_leaf_bones,
        # Animation
        bake_anim=addon_props.cbb_export_bake_anim,
        bake_anim_use_nla_strips=addon_props.cbb_export_use_nla_strips,
        bake_anim_use_all_actions=addon_props.cbb_export_use_all_actions,
    )


def get_actions_from_objects(selected_objects: list) -> list:
    actions = []
    for obj in selected_objects:
        if obj.type == "ARMATURE" and obj.animation_data.action:
            action = obj.animation_data.action
            actions.append(action)
            bpy.data.actions.append(action)
    return actions


def delete_objects(objects: list) -> None:
    for obj in objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    # Update the scene to reflect the changes
    bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)


def apply_action(armature, action, action_name="cascadeur_action") -> None:
    action.name = action_name
    if not hasattr(armature.animation_data, "action"):
        armature.animation_data_create()
    armature.animation_data.action = action


class CBB_OT_export_blender_fbx(bpy.types.Operator):
    """Exports the selected objects and imports them to Cascadeur"""

    bl_idname = "cbb.export_blender_fbx"
    bl_label = "Export to Cascadeur"

    server_socket = None
    file_path = None

    @classmethod
    def poll(cls, context):
        return addon_info.operation_completed

    def __del__(self):
        self.server_socket.close()
        addon_info.operation_completed = True

    def modal(self, context, event):
        if event.type == "ESC":
            addon_info.operation_completed = True
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
        addon_info.operation_completed = False
        self.server_socket = ServerSocket()

        self.file_path = file_handling.get_export_path()
        try:
            export_fbx(self.file_path)
        except Exception as e:
            self.report({"ERROR"}, "Couldn't export fbx file")
            addon_info.operation_completed = True
            return {"CANCELLED"}
        CascadeurHandler().execute_csc_command("commands.externals.temp_importer")
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


class CBB_OT_import_cascadeur_fbx(bpy.types.Operator):
    """Imports the currently opened Cascadeur scene"""

    bl_idname = "cbb.import_cascadeur_fbx"
    bl_label = "Import Cascadeur Scene"

    server_socket = None

    @classmethod
    def poll(cls, context):
        return addon_info.operation_completed

    batch_export: bpy.props.BoolProperty(
        name="Import all scene",
        description="",
        default=False,
    )

    def __del__(self):
        self.server_socket.close()
        addon_info.operation_completed = True

    def modal(self, context, event):
        if event.type == "ESC":
            addon_info.operation_completed = True
            return {"CANCELLED"}

        self.server_socket.run()

        if self.server_socket.client_socket:
            self.server_socket.send_message(get_csc_export_settings())
            data = self.server_socket.receive_message()
            if data:
                print(str(data))
                if not isinstance(data, list):
                    self.report({"ERROR"}, f"Unexpected response: {str(data)}")
                    addon_info.operation_completed = True
                    return {"CANCELLED"}

                for file in data:
                    import_fbx(file)
                    file_handling.delete_file(file)
                self.report({"INFO"}, "Finished")
                return {"FINISHED"}

        return {"PASS_THROUGH"}

    def execute(self, context):
        addon_info.operation_completed = False
        self.server_socket = ServerSocket()
        command_file = "temp_batch_exporter" if self.batch_export else "temp_exporter"
        CascadeurHandler().execute_csc_command(f"commands.externals.{command_file}")
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


class CBB_OT_import_action_to_selected(bpy.types.Operator):
    """Imports the action from Cascadeur and apply to selected armature"""

    bl_idname = "cbb.import_cascadeur_action"
    bl_label = "Import Cascadeur Action"

    ao = None
    imported_objects = []

    @classmethod
    def poll(cls, context):
        return (
            context.active_object
            and context.selected_objects
            and context.active_object.type == "ARMATURE"
            and addon_info.operation_completed
        )

    batch_export: bpy.props.BoolProperty(
        name="Import all scene",
        description="",
        default=False,
    )

    def __del__(self):
        self.server_socket.close()
        addon_info.operation_completed = True

    def modal(self, context, event):
        if event.type == "ESC":
            addon_info.operation_completed = True
            return {"CANCELLED"}

        self.server_socket.run()

        if self.server_socket.client_socket:
            self.server_socket.send_message(get_csc_export_settings())
            data = self.server_socket.receive_message()
            if data:
                print(str(data))
                if not isinstance(data, list):
                    self.report({"ERROR"}, f"Unexpected response: {str(data)}")
                    addon_info.operation_completed = True
                    return {"CANCELLED"}

                for file in data:
                    objects = import_fbx(file)
                    self.imported_objects.extend(objects)
                    scene_name = os.path.splitext(os.path.basename(file))[0]
                    file_handling.delete_file(file)
                    actions = get_actions_from_objects(objects)
                    apply_action(self.ao, actions[0], scene_name)
                delete_objects(self.imported_objects)

                self.ao.select_set(True)
                bpy.context.view_layer.objects.active = self.ao
                self.report({"INFO"}, "Finished")
                return {"FINISHED"}

        return {"PASS_THROUGH"}

    def execute(self, context):
        addon_info.operation_completed = False
        self.ao = bpy.context.active_object
        self.server_socket = ServerSocket()
        command_file = "temp_batch_exporter" if self.batch_export else "temp_exporter"
        CascadeurHandler().execute_csc_command(f"commands.externals.{command_file}")
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
