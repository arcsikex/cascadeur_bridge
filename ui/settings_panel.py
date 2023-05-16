import bpy
from .main_panel import PanelBasics


class CBB_PT_csc_bridge_settings(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_csc_bridge_settings"
    bl_label = "Settings"
    bl_parent_id = "CBB_PT_parent"

    def draw_header(self, context):
        self.layout.label(text="", icon="SETTINGS")

    def draw(self, context):
        layout = self.layout
        row = layout.row()


class CBB_PT_csc_export_settings(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_csc_export_settings"
    bl_label = "Cascadeur Export Settings"
    bl_parent_id = "CBB_PT_csc_bridge_settings"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        addon_props = context.scene.cbb_fbx_settings
        layout = self.layout
        box = layout.box()
        box.label(text="Cascadeur FBX export settings")
        col = box.column(align=True)
        col.prop(addon_props, "cbb_csc_import_selected")
        col.prop(addon_props, "cbb_csc_apply_euler_filter")
        col.prop(addon_props, "cbb_csc_up_axis")
        col.prop(addon_props, "cbb_csc_bake_animation")


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
