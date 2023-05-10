import bpy
from .main_panel import PanelBasics


class CBB_PT_csc_bridge_settings(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_csc_bridge_settings"
    bl_label = "Settings"
    bl_parent_id = "CBB_PT_parent"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="MODIFIER_DATA")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Save settings")
        row.label(text="Reset settings")


class CBB_PT_csc_export_settings(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_csc_export_settings"
    bl_label = "Cascadeur Export Settings"
    bl_parent_id = "CBB_PT_csc_bridge_settings"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Options for Cascadeur FBX export")


class CBB_PT_blender_export_settings(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_blender_export_settings"
    bl_label = "Blender Export Settings"
    bl_parent_id = "CBB_PT_csc_bridge_settings"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Options for Blender FBX export")


class CBB_PT_blender_import_settings(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_blender_import_settings"
    bl_label = "Blender Import Settings"
    bl_parent_id = "CBB_PT_csc_bridge_settings"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Options for Blender FBX import")
