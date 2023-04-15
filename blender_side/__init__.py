bl_info = {
    "name": "Cascadeur to Blender",
    "author": "Aron Nemeth",
    "version": (0, 1),
    "blender": (3, 5, 0),
    "location": "View3D > Panels > csc2blend",
    "description": "Helps you import animations from Cascadeur",
    "doc_url": "https://github.com/arcsikex/cacs-to-blender",
    "tracker_url": "https://github.com/arcsikex/cacs-to-blender/issues",
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


from .utils import csc_handling, file_handling


class CT_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    _csc_path = csc_handling.get_default_csc_path()

    csc_exe_path: bpy.props.StringProperty(
        name="File Path",
        subtype="FILE_PATH",
        default=_csc_path if file_handling.file_exists(_csc_path) else "",
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
