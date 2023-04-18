import bpy

from ..utils import file_handling
from ..utils.csc_handling import CascadeurHandler
from . import reciever


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


class CT_OT_import_cascadeur_fbx(bpy.types.Operator):
    """Imports the currently opened Cascadeur scene"""

    bl_idname = "ct.import_cascadeur_fbx"
    bl_label = "Import Cascadeur Scene"

    def execute(self, context):
        CascadeurHandler().execute_csc_command("commands.external.temp_export.py")
        bpy.ops.ct.start_server()
        data = reciever.recieved_data
        if data:
            import_fbx(data)
            file_handling.delete_file(data)
            reciever.recieved_data = None
        else:
            return {"CANCELLED"}
        return {"FINISHED"}


class CT_OT_import_action_to_selected(bpy.types.Operator):
    """Imports the action from Cascadeur and apply to selected armature"""

    bl_idname = "ct.import_cascadeur_action"
    bl_label = "Import Cascadeur Action"

    @classmethod
    def poll(cls, context):
        return (
            context.active_object
            and context.selected_objects
            and context.active_object.type == "ARMATURE"
        )

    def execute(self, context):
        ao = bpy.context.active_object
        CascadeurHandler().execute_csc_command("commands.external.temp_export.py")
        bpy.ops.ct.start_server()
        data = reciever.recieved_data
        if data:
            imported_objects = import_fbx(data)
            file_handling.delete_file(data)
            reciever.recieved_data = None
        else:
            print("No data recieved")
            return {"CANCELLED"}

        actions = get_actions_from_objects(imported_objects)
        apply_action(ao, actions)
        delete_objects(imported_objects)
        return {"FINISHED"}


# Should be moved to a different place
class CT_OT_start_cascadeur(bpy.types.Operator):
    """Start Cascadeur"""

    bl_idname = "ct.start_cascadeur"
    bl_label = "Start Cascadeur"

    @classmethod
    def poll(cls, context):
        return CascadeurHandler().is_csc_exe_path_valid

    def execute(self, context):
        CascadeurHandler().start_cascadeur()
        return {"FINISHED"}
