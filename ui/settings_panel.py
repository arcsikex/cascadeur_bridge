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
        row.operator(
            "cbb.save_fbx_settings",
            text="Save Settings",
            icon="FAKE_USER_ON",
        )
        row.separator()


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
        col.prop(addon_props, "cbb_csc_apply_euler_filter")
        col.prop(addon_props, "cbb_csc_up_axis")
        col.prop(addon_props, "cbb_csc_bake_animation")


class CBB_PT_blender_export_settings(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_blender_export_settings"
    bl_label = "Blender Export Settings"
    bl_parent_id = "CBB_PT_csc_bridge_settings"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        addon_props = context.scene.cbb_fbx_settings
        layout = self.layout
        box = layout.box()
        box.label(text="Include")
        col = box.column(align=True)
        col.prop(addon_props, "cbb_export_use_selection")
        col.prop(addon_props, "cbb_export_object_types")

        box = layout.box()
        box.label(text="Transform")
        col = box.column(align=True)
        col.prop(addon_props, "cbb_export_global_scale")
        col.prop(addon_props, "cbb_export_axis_forward")
        col.prop(addon_props, "cbb_export_axis_up")
        col.prop(addon_props, "cbb_export_apply_transform")

        box = layout.box()
        box.label(text="Armature")
        col = box.column(align=True)
        col.prop(addon_props, "cbb_export_primary_bone_axis")
        col.prop(addon_props, "cbb_export_secondary_bone_axis")
        col.prop(addon_props, "cbb_export_deform_only")
        col.prop(addon_props, "cbb_export_leaf_bones")

        box = layout.box()
        box.label(text="Animation")
        col = box.column(align=True)
        col.prop(addon_props, "cbb_export_bake_anim")
        col.prop(addon_props, "cbb_export_use_nla_strips")
        col.prop(addon_props, "cbb_export_use_all_actions")


class CBB_PT_blender_import_settings(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_blender_import_settings"
    bl_label = "Blender Import Settings"
    bl_parent_id = "CBB_PT_csc_bridge_settings"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        addon_props = context.scene.cbb_fbx_settings
        layout = self.layout
        box = layout.box()
        box.label(text="Transform")
        col = box.column(align=True)
        col.prop(addon_props, "cbb_import_global_scale")
        col.prop(addon_props, "cbb_import_apply_transform")
        col.prop(addon_props, "cbb_import_manual_orientation")
        col.prop(addon_props, "cbb_import_axis_forward")
        col.prop(addon_props, "cbb_import_axis_up")

        box = layout.box()
        box.label(text="Animation")
        col = box.column(align=True)
        col.prop(addon_props, "cbb_import_use_anim")
        col.prop(addon_props, "cbb_import_anim_offset")

        box = layout.box()
        box.label(text="Armature")
        col = box.column(align=True)
        col.prop(addon_props, "cbb_import_ignore_leaf_bones")
        col.prop(addon_props, "cbb_import_force_connect_children")
        col.prop(addon_props, "cbb_import_automatic_bone_orientation")
        col.prop(addon_props, "cbb_import_primary_bone_axis")
        col.prop(addon_props, "cbb_import_secondary_bone_axis")
        col.prop(addon_props, "cbb_import_use_prepost_rot")
