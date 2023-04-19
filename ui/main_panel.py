import bpy
from ..utils.csc_handling import CascadeurHandler
from ..utils import file_handling


class PanelBasics:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CSC Bridge"


class CBB_PT_parent_panel(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_parent"
    bl_label = "Cascadeur Bridge"

    def draw_header(self, context):
        self.layout.label(text="", icon="MODIFIER_DATA")

    def draw(self, context):
        _ch = CascadeurHandler()
        layout = self.layout
        col = layout.column(align=False)
        if not _ch.is_csc_exe_path_valid:
            col.label(
                icon="ERROR", text="Set a valid Cascadeur exe path in preferences!"
            )
            col.separator()

        if not file_handling.commands_installed() or not file_handling.pyds_installed():
            col.label(icon="ERROR", text="Install necessary files for Cascadeur!")
            col.separator()

        col.operator(
            "cbb.start_cascadeur",
            text="Start Cascadeur",
            icon="MESH_UVSPHERE",
        )


class CBB_PT_csc_to_blender(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_csc_to_blender"
    bl_label = "Cascadeur -> Blender"
    bl_parent_id = "CBB_PT_parent"

    """
    def draw_header(self, context):
        self.layout.label(text="", icon="")
    """

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        # Operations Layout
        col.operator(
            "cbb.import_cascadeur_action",
            text="Import Action",
            icon="IMPORT",
        )

        col.operator(
            "cbb.import_cascadeur_fbx",
            text="Import Scene",
            icon="IMPORT",
        )
