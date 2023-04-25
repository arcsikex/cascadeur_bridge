import bpy
from .main_panel import PanelBasics


class CBB_PT_csc_bridge_info(PanelBasics, bpy.types.Panel):
    bl_idname = "CBB_PT_csc_bridge_info"
    bl_label = "Information"
    bl_parent_id = "CBB_PT_parent"

    def draw_header(self, context):
        self.layout.label(text="", icon="INFO")

    def draw(self, context):
        layout = self.layout

        # Box - Social
        box = layout.box()
        box.label(text="Social")
        column = box.column()

        row = column.row(align=True)
        row.scale_y = 1.2
        row.operator(
            "wm.url_open", text="YouTube", icon="FILE_MOVIE"
        ).url = "https://www.youtube.com/c/AronNemeth95"
        row.operator(
            "wm.url_open", text="GitHub", icon="SCRIPT"
        ).url = "https://github.com/arcsikex/cascadeur_bridge"
        row = column.row()
        row.scale_y = 1.5
