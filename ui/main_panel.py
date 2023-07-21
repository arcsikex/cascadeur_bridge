import bpy
from ..utils.csc_handling import CascadeurHandler
from ..utils.config_handling import get_panel_name
from .. import addon_info


class PanelBasics:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = get_panel_name()


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

        row = col.row()

        row.operator(
            "cbb.start_cascadeur",
            text="Start Cascadeur",
            icon="MESH_UVSPHERE",
        )
        row.scale_y = 1.5
        col.separator()

        if not addon_info.operation_completed:
            col.label(icon="LOCKED", text="Operation in progress!")
            col.separator()

        # Blender to Cascadeur
        box = layout.box()
        col = box.column(align=True)
        row = col.row()
        row.label(text="Blender > Cascadeur")
        row.scale_y = 1.2

        col.operator(
            "cbb.export_blender_fbx", text="Export To Cascadeur", icon="EXPORT"
        )
        # Cascadeur to Blender
        box = layout.box()
        col = box.column(align=True)
        row = col.row()
        row.label(text="Cascadeur > Blender")
        row.scale_y = 1.2

        props = col.operator(
            "cbb.import_cascadeur_action",
            text="Import Action",
            icon="ARMATURE_DATA",
        )
        props.batch_export = False
        props = col.operator(
            "cbb.import_cascadeur_fbx",
            text="Import Scene",
            icon="IMPORT",
        )
        props.batch_export = False
        # Batch
        col = box.column(align=True)
        col.label(text="Batch Import")
        props = col.operator(
            "cbb.import_cascadeur_action",
            text="Import All Actions",
            icon="CON_ARMATURE",
        )
        props.batch_export = True
        props = col.operator(
            "cbb.import_cascadeur_fbx",
            text="Import All Scenes",
            icon="DOCUMENTS",
        )
        props.batch_export = True
