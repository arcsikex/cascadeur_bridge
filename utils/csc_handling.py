import subprocess
import os

from . import file_handling

import bpy


class CascadeurHandler:
    @property
    def csc_exe_path_addon_preference(self) -> str:
        preferences = bpy.context.preferences
        addon_prefs = preferences.addons["cascadeur_bridge"].preferences
        return addon_prefs.csc_exe_path

    @property
    def csc_dir(self):
        if self.is_csc_exe_path_valid:
            return os.path.dirname(self.csc_exe_path_addon_preference)

    @property
    def is_csc_exe_path_valid(self) -> bool:
        csc_path = self.csc_exe_path_addon_preference
        return True if csc_path and file_handling.file_exists(csc_path) else False

    @property
    def commands_path(self) -> str:

        commands_config = os.path.join(self.csc_dir, "resources", "settings.ini")
        with open(commands_config, "r") as f:
            for line in f:
                if line.startswith("ScriptsDir"):
                    scripts_dir = line.split("=")[1].strip().strip('"')
                    break
        if scripts_dir:
            return scripts_dir
        else:
            return os.path.join(
                self.csc_dir, "resources", "scripts", "python", "commands"
            )

    def start_cascadeur(self) -> None:
        csc_path = self.csc_exe_path_addon_preference
        subprocess.Popen([csc_path])

    def execute_csc_command(self, command: str) -> None:
        subprocess.Popen([self.csc_exe_path_addon_preference, command])
