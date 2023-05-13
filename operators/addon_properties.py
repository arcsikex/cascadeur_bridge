import bpy


class CBB_PG_fbx_settings(bpy.types.PropertyGroup):
    # Cascadeur Export settings
    cbb_import_selected: bpy.props.BoolProperty(
        name="Selected Interval",
        description="Import selected interval only",
        default=False,
    )

    cbb_apply_euler_filter: bpy.props.BoolProperty(
        name="Apply Euler Filter",
        description="Import selected interval only",
        default=False,
    )

    cbb_csc_up_axis: bpy.props.EnumProperty(
        items=[("Y", "Y", "", 1), ("Z", "Z", "", 1)],
        name="Up Axis",
        description="Up Axis when exporting from Cascadeur",
        default="Y",
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
    settings["selected_interval"] = addon_props.cbb_import_selected
    settings["euler_filter"] = addon_props.cbb_apply_euler_filter
    settings["up_axis"] = addon_props.cbb_csc_up_axis
    return settings
