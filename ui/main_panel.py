import bpy
from ..utils.csc_handling import CascadeurHandler


class PanelBasics:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CSC Tools"


class WS_PT_parent_panel(PanelBasics, bpy.types.Panel):
    bl_idname = "CT_PT_parent"
    bl_label = "Cascadeur Tools"

    def draw_header(self, context):
        self.layout.label(text="", icon="MODIFIER_DATA")

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=False)
        if not CascadeurHandler().is_csc_exe_path_valid:
            col.label(
                icon="ERROR", text="Set a valid Cascadeur exe path in preferences!"
            )
            col.separator()
        col.operator(
            "ct.start_cascadeur",
            text="Start Cascadeur",
            icon="MESH_UVSPHERE",
        )


class WS_PT_csc_to_blender(PanelBasics, bpy.types.Panel):
    bl_idname = "CT_PT_csc_to_blender"
    bl_label = "Cascadeur -> Blender"
    bl_parent_id = "CT_PT_parent"

    """
    def draw_header(self, context):
        self.layout.label(text="", icon="")
    """

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        # Operations Layout
        col.operator(
            "ct.import_cascadeur_action",
            text="Import Action",
            icon="IMPORT",
        )

        col.operator(
            "ct.import_cascadeur_fbx",
            text="Import Scene",
            icon="IMPORT",
        )
