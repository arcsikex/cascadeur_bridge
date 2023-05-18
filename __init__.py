bl_info = {
    "name": "Cascadeur Bridge for Blender",
    "author": "Aron Nemeth",
    "version": (0, 7, 0),
    "blender": (3, 5, 0),
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
import platform

from .utils import file_handling


class CBB_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    @staticmethod
    def default_csc_exe_path() -> str:
        csc_path = {
            "Windows": r"C:\Program Files\Cascadeur\cascadeur.exe",
            "Linux": r"/opt/cascadeur/cascadeur",
        }
        default = csc_path.get(platform.system(), "")
        return default if file_handling.file_exists(default) else ""

    csc_exe_path: bpy.props.StringProperty(
        name="Cascadeur executable",
        subtype="FILE_PATH",
        default=default_csc_exe_path(),
    )

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=False)
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
