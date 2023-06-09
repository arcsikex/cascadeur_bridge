import bpy
import os

from ..utils import file_handling
from ..utils.csc_handling import CascadeurHandler
from .. import addon_info


class CBB_OT_start_cascadeur(bpy.types.Operator):
    """Start Cascadeur"""

    bl_idname = "cbb.start_cascadeur"
    bl_label = "Start Cascadeur"

    @classmethod
    def poll(cls, context):
        return CascadeurHandler().is_csc_exe_path_valid

    def execute(self, context):
        CascadeurHandler().start_cascadeur()
        addon_info.operation_completed = True
        return {"FINISHED"}


class CBB_OT_install_required_files(bpy.types.Operator):
    """Copy the necessary python script to Cascadeurs folder"""

    bl_idname = "cbb.install_required_files"
    bl_label = "Install Required Files"

    @classmethod
    def poll(cls, context):
        return CascadeurHandler().is_csc_exe_path_valid

    def execute(self, context):
        ch = CascadeurHandler()
        # Copy commands
        commands_source = os.path.join(addon_info.ADDON_PATH, "csc_files", "externals")
        commands_path = os.path.join(ch.commands_path, "externals")
        result = file_handling.copy_files(
            commands_source, commands_path, os.listdir(commands_source)
        )
        if not result:
            self.report(
                {"ERROR"}, "You don't have permission to copy the files for Cascadeur"
            )
            self.report({"INFO"}, "Restart Blender as Admin and try again")
            return {"CANCELLED"}
        self.report({"INFO"}, "All necessary files have been successfully copied")
        return {"FINISHED"}
