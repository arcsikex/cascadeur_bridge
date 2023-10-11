bl_info = {
    "name": "Cascadeur Bridge for Blender",
    "author": "Aron Nemeth",
    "version": (1, 0, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Panels > CSC Bridge",
    "description": "Helps you to integrate Cascadeur to your workflow with Belnder.",
    "doc_url": "https://github.com/arcsikex/cascadeur_bridge",
    "tracker_url": "https://github.com/arcsikex/cascadeur_bridge/issues",
    "category": "Animation",
}

if "bpy" not in locals():
    from . import operators
    from . import ui
else:
    import importlib

    importlib.reload(operators)
    importlib.reload(ui)

import bpy

from .utils import config_handling
from .utils.csc_handling import get_default_csc_exe_path


def update_all_tab_names(self, context):
    try:
        # Unregister everything
        for c in ui.classes:
            bpy.utils.unregister_class(c)
    except:
        pass

    # Set panel name for base class
    new_name = bpy.context.preferences.addons[__name__].preferences.csc_tab_name
    ui.main_panel.PanelBasics.bl_category = new_name
    # Save to file
    config_handling.set_config_parameter("Addon Settings", "panel_name", new_name)

    # Register everything
    for c in ui.classes:
        bpy.utils.register_class(c)


class CBB_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    csc_exe_path: bpy.props.StringProperty(
        name="Cascadeur executable",
        subtype="FILE_PATH",
        default=get_default_csc_exe_path(),
    )

    csc_tab_name: bpy.props.StringProperty(
        name="N Panel Name",
        description="Name of the add-on on the N Panel",
        default=config_handling.get_panel_name(),
        update=update_all_tab_names,
    )

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=False)
        row = col.row()
        row.prop(self, "csc_tab_name")
        col.separator()
        row = col.row()
        row.prop(self, "csc_exe_path")
        row = col.row()
        row.operator(
            "cbb.install_required_files",
            text="Install Requirements",
            icon="MODIFIER",
        )


classes = [CBB_preferences] + operators.classes + ui.classes


def register():
    operators.addon_properties.register_props()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    operators.addon_properties.unregister_props()
    for cls in classes:
        bpy.utils.unregister_class(cls)
