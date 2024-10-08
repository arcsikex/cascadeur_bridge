import bpy
from ..utils import config_handling


def generate_items(options: list) -> list:
    return [(option, option, "") for option in options]


class CBB_PG_fbx_settings(bpy.types.PropertyGroup):
    # Cascadeur Export settings
    cbb_csc_import_selected: bpy.props.BoolProperty(
        name="Selected Interval",
        description="Import selected interval only",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_csc_import_selected",
            bool,
            fallback=False,
        ),
    )

    cbb_csc_apply_euler_filter: bpy.props.BoolProperty(
        name="Apply Euler Filter",
        description="Automatically set objects' rotations to lowes possible values",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_csc_apply_euler_filter",
            bool,
            fallback=False,
        ),
    )

    cbb_csc_up_axis: bpy.props.EnumProperty(
        items=generate_items(["Y", "Z"]),
        name="Up Axis",
        description="Up Axis when exporting from Cascadeur",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_csc_up_axis",
            str,
            fallback="Y",
        ),
    )

    cbb_csc_bake_animation: bpy.props.BoolProperty(
        name="Bake animation",
        description="Key all frames when exporting from Cascadeur",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_csc_bake_animation",
            bool,
            fallback=True,
        ),
    )

    # Blender Import settings
    cbb_import_global_scale: bpy.props.FloatProperty(
        name="Global Scale",
        description="Scale",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_global_scale",
            float,
            fallback=1.0,
        ),
        min=0.001,
        max=1000,
    )

    cbb_import_apply_transform: bpy.props.BoolProperty(
        name="Apply Transform",
        description="Bake space transform into object data. EXPERIMENTAL!",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_apply_transform",
            bool,
            fallback=False,
        ),
    )

    cbb_import_manual_orientation: bpy.props.BoolProperty(
        name="Use Manual Orientation",
        description="Specify orientation and scale, instead of using embedded data in FBX file",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_manual_orientation",
            bool,
            fallback=False,
        ),
    )

    cbb_import_axis_forward: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Forward",
        description="Forward Axis",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_axis_forward",
            str,
            fallback="-Z",
        ),
    )

    cbb_import_axis_up: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Up",
        description="Forward Up",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_axis_up",
            str,
            fallback="Y",
        ),
    )

    cbb_import_use_anim: bpy.props.BoolProperty(
        name="Import Animation",
        description="Import FBX animation",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_use_anim",
            bool,
            fallback=True,
        ),
    )

    cbb_import_anim_offset: bpy.props.FloatProperty(
        name="Animation Offset",
        description=" Offset to apply to animation during import, in frames",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_anim_offset",
            float,
            fallback=1.0,
        ),
    )

    cbb_import_ignore_leaf_bones: bpy.props.BoolProperty(
        name="Ignore Leaf Bones",
        description="Ignore the last bone at the end of each chain",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_ignore_leaf_bones",
            bool,
            fallback=True,
        ),
    )

    cbb_import_force_connect_children: bpy.props.BoolProperty(
        name="Force Connect Children",
        description="Force connection of children bones to their parent",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_force_connect_children",
            bool,
            fallback=False,
        ),
    )

    cbb_import_automatic_bone_orientation: bpy.props.BoolProperty(
        name="Automatic Bone Orientation",
        description="Try to align the major bone axis with the bone children",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_automatic_bone_orientation",
            bool,
            fallback=False,
        ),
    )

    cbb_import_primary_bone_axis: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Primary Bone Axis",
        description="",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_primary_bone_axis",
            str,
            fallback="Y",
        ),
    )

    cbb_import_secondary_bone_axis: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Secondary Bone Axis",
        description="",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_secondary_bone_axis",
            str,
            fallback="X",
        ),
    )

    cbb_import_use_prepost_rot: bpy.props.BoolProperty(
        name="Use Pre/Post Rotation",
        description="Use pre/post rotation from FBX transform",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_use_prepost_rot",
            bool,
            fallback=True,
        ),
    )

    # Blender Export settings
    cbb_export_use_selection: bpy.props.BoolProperty(
        name="Selected Objects",
        description="Export selected and visible objects only",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_use_selection",
            bool,
            fallback=False,
        ),
    )

    cbb_export_object_types: bpy.props.EnumProperty(
        name="Object Types",
        options={"ENUM_FLAG"},
        items=(
            ("EMPTY", "Empty", ""),
            ("CAMERA", "Camera", ""),
            ("LIGHT", "Lamp", ""),
            ("ARMATURE", "Armature", "WARNING: not supported in dupli/group instances"),
            ("MESH", "Mesh", ""),
            (
                "OTHER",
                "Other",
                "Other geometry types, like curve, metaball, etc. (converted to meshes)",
            ),
        ),
        description="Which kind of object to export",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_object_types",
            set,
            fallback={"EMPTY", "CAMERA", "LIGHT", "ARMATURE", "MESH", "OTHER"},
        ),
    )

    cbb_export_global_scale: bpy.props.FloatProperty(
        name="Global Scale",
        description="Scale",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_global_scale",
            float,
            fallback=1.0,
        ),
        min=0.001,
        max=1000,
    )

    cbb_export_axis_forward: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Forward",
        description="Forward Axis",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_axis_forward",
            str,
            fallback="-Z",
        ),
    )

    cbb_export_axis_up: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Up",
        description="Forward Up",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_axis_up",
            str,
            fallback="Y",
        ),
    )

    cbb_export_apply_transform: bpy.props.BoolProperty(
        name="Apply Transform",
        description="Bake space transform into object data. EXPERIMENTAL!",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_apply_transform",
            bool,
            fallback=False,
        ),
    )

    cbb_export_primary_bone_axis: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Primary Bone Axis",
        description="",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_primary_bone_axis",
            str,
            fallback="Y",
        ),
    )

    cbb_export_secondary_bone_axis: bpy.props.EnumProperty(
        items=generate_items(["X", "Y", "Z", "-X", "-Y", "-Z"]),
        name="Secondary Bone Axis",
        description="",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_secondary_bone_axis",
            str,
            fallback="X",
        ),
    )

    cbb_export_deform_only: bpy.props.BoolProperty(
        name="Only Deform Bones",
        description="Only write deforming bones",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_deform_only",
            bool,
            fallback=True,
        ),
    )

    cbb_export_leaf_bones: bpy.props.BoolProperty(
        name="Add Leaf Bones",
        description="Append a final bone to the end of each chain to specify last bone length",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_leaf_bones",
            bool,
            fallback=False,
        ),
    )

    cbb_export_bake_anim: bpy.props.BoolProperty(
        name="Baked Animation",
        description="Export baked keyframe animation",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_bake_anim",
            bool,
            fallback=True,
        ),
    )

    cbb_export_use_nla_strips: bpy.props.BoolProperty(
        name="NLA Strips",
        description="Export each non-muted NLA strip as a separated FBX’s AnimStack, if any, instead of global scene animation",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_use_nla_strips",
            bool,
            fallback=False,
        ),
    )

    cbb_export_use_all_actions: bpy.props.BoolProperty(
        name="All Actions",
        description="Export each action as a separated FBX’s AnimStack, instead of global scene animation",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_use_all_actions",
            bool,
            fallback=False,
        ),
    )

    cbb_export_methods: bpy.props.EnumProperty(
        name="Cascadeur Export Method",
        items=(
            ("export_all_objects", "Export All Objects", ""),
            ("export_joints", "Animation", ""),
            ("export_joints_selected", "Animation - selected joints and frames", ""),
            ("export_joints_selected_frames", "Animation - selected frames", ""),
            ("export_joints_selected_objects", "Animation - selected joints", ""),
            ("export_model", "Model", ""),
            ("export_scene_selected", "Scene - selected objects and frames", ""),
            ("export_scene_selected_frames", "Scene - selected frames", ""),
            ("export_scene_selected_objects", "Scene - selected objects", ""),
        ),
        description="Method to use when exporting from Cascadeur",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_export_methods",
            str,
            fallback="export_all_objects",
        ),
    )  # type: ignore

    cbb_import_methods: bpy.props.EnumProperty(
        name="Cascadeur Import Method",
        items=(
            ("add_model", "Add Model", ""),
            ("add_model_to_selected", "Add Model to Selected", ""),
            ("import_animation", "Animation", ""),
            ("import_animation_to_selected_frames", "Animation - selected frames", ""),
            ("import_animation_to_selected_objects", "Animation - selected joints", ""),
            ("import_model", "Model", ""),
            ("import_scene", "Scene", ""),
        ),
        description="Method to use when exporting from Cascadeur",
        default=config_handling.get_config_parameter(
            "FBX Settings",
            "cbb_import_methods",
            str,
            fallback="import_model",
        ),
    )  # type: ignore

    cbb_port: bpy.props.IntProperty(
        name="Port",
        description="Port number used for communicating with Cascadeur",
        default=config_handling.get_config_parameter(
            "Addon Settings",
            "port",
            int,
            fallback=53145,
        ),
        min=0,
        max=65535,
    )


def register_props():
    bpy.utils.register_class(CBB_PG_fbx_settings)
    bpy.types.Scene.cbb_fbx_settings = bpy.props.PointerProperty(
        type=CBB_PG_fbx_settings
    )


def unregister_props():
    bpy.utils.unregister_class(CBB_PG_fbx_settings)


def get_csc_export_settings() -> dict:
    settings = {}
    addon_props = bpy.context.scene.cbb_fbx_settings
    settings["selected_interval"] = addon_props.cbb_csc_import_selected
    settings["euler_filter"] = addon_props.cbb_csc_apply_euler_filter
    settings["up_axis"] = addon_props.cbb_csc_up_axis
    settings["bake_animation"] = addon_props.cbb_csc_bake_animation
    settings["export_method"] = addon_props.cbb_export_methods
    return settings


class CBB_OT_save_fbx_settings(bpy.types.Operator):
    """Save fbx import and export settings for Cascadeur and Blender"""

    bl_idname = "cbb.save_fbx_settings"
    bl_label = "Save Settings for CSC Bridge"

    def execute(self, context):
        try:
            config_handling.save_fbx_settings()
        except Exception as e:
            self.report({"ERROR", f"Couldn't save settings: {e}"})
            return {"CANCELLED"}
        self.report({"INFO"}, "Settings saved")
        return {"FINISHED"}


class CBB_OT_reset_fbx_settings(bpy.types.Operator):
    """Reset fbx import and export settings for Cascadeur and Blender"""

    bl_idname = "cbb.reset_fbx_settings"
    bl_label = "Reset FBX Settings of CSC Bridge"

    def execute(self, context):
        try:
            config_handling.reset_fbx_settings()
            # Update UI panel
            bpy.context.area.tag_redraw()
        except Exception as e:
            self.report({"ERROR", f"Couldn't save settings: {e}"})
            return {"CANCELLED"}
        self.report({"INFO"}, "Settings reset")
        return {"FINISHED"}


class CBB_OT_save_port_number(bpy.types.Operator):
    """Save port settings for Cascadeur and Blender"""

    bl_idname = "cbb.save_port_settings"
    bl_label = "Save Port"

    def execute(self, context):
        result = config_handling.save_port_number()

        if not result:
            self.report(
                {"ERROR"}, "You don't have permission to write the config file."
            )
            self.report({"INFO"}, "Restart Blender as Admin and try again")
            return {"CANCELLED"}
        self.report({"INFO"}, "Settings saved")
        return {"FINISHED"}
