import bpy


class WS_PT_Workspaces_Info_Panel(bpy.types.Panel):
    bl_idname = "WS_PT_Workspaces_Info_Panel"
    bl_label = "Information"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Workspaces"
    bl_parent_id = "WS_PT_Parent_Panel"

    def draw_header(self, context):
        self.layout.label(text="", icon="INFO")

    def draw(self, context):
        layout = self.layout

        # Operations Layout
        box = layout.box()
        column = box.column()
        column.label(text="Created by Curtis Holt")

        # ---------- Box - Social
        b = box.box()
        b.label(text="Social")
        column = b.column()

        row = column.row()
        row.scale_y = 1.2
        row.operator(
            "wm.url_open", text="YouTube", icon="FILE_MOVIE"
        ).url = "https://www.youtube.com/c/AronNemeth95"
        row.operator(
            "wm.url_open", text="GitHub", icon="SCRIPT"
        ).url = "https://github.com/arcsikex/cacs-to-blender"
