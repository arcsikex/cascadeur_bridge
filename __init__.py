bl_info = {
    "name": "Cascadeur Bridge for Blender",
    "author": "Aron Nemeth",
    "version": (0, 3),
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
import os

ADDON_PATH = os.path.abspath(__file__)


class CBB_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    @staticmethod
    def default_csc_exe_path() -> str:
        csc_path = {
            "Windows": r"C:\Program Files\Cascadeur\cascadeur.exe",
        }
        return csc_path.get(platform.system(), "")

    csc_exe_path: bpy.props.StringProperty(
        name="File Path",
        subtype="FILE_PATH",
        default=default_csc_exe_path(),
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Cascadeur Executable path:")
        layout.prop(self, "csc_exe_path")


classes = [CBB_preferences] + operators.classes + ui.classes


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
