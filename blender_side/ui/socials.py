import bpy
from .main_panel import PanelBasics


class WS_PT_csc_tools_info(PanelBasics, bpy.types.Panel):
    bl_idname = "CT_PT_csc_tools_info"
    bl_label = "Information"
    bl_parent_id = "CT_PT_parent"

    def draw_header(self, context):
        self.layout.label(text="", icon="INFO")

    def draw(self, context):
        layout = self.layout

        # Operations Layout
        box = layout.box()
        column = box.column()
        column.label(text="Created by Aron Nemeth")

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
