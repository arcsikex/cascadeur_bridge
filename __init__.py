bl_info = {
    "name": "Cascadeur to Blender",
    "author": "Aron Nemeth",
    "version": (0, 1),
    "blender": (3, 5, 0),
    "location": "View3D > Panels > csc2blend",
    "description": "Helps you import animations from Cascadeur",
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


from .utils.csc_handling import CascadeurHandler


class CT_preferences(bpy.types.AddonPreferences):
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


classes = [CT_preferences] + operators.classes + ui.classes


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
