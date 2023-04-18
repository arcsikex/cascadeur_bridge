import platform
import subprocess
import configparser
import os

from . import file_handling

import bpy


class CascadeurHandler:
    @property
    def default_csc_exe_path(self) -> str:
        csc_path = {
            "Windows": r"C:\Program Files\Cascadeur\cascadeur.exe",
        }
        return csc_path.get(platform.system(), "")

    @property
    def csc_exe_path_addon_preference(self) -> str:
        preferences = bpy.context.preferences
        addon_prefs = preferences.addons["cascadeur_bridge"].preferences
        return addon_prefs.csc_exe_path

    @property
    def is_csc_exe_path_valid(self) -> bool:
        csc_path = self.csc_exe_path_addon_preference
        return True if csc_path and file_handling.file_exists(csc_path) else False

    @property
    def csc_dir(self):
        if self.is_csc_exe_path_valid:
            return os.path.dirname(self.csc_exe_path_addon_preference)

    @property
    def commands_path(self) -> str:
        config = configparser.ConfigParser()
        config.read(os.path.join(self.csc_dir, "resources", "settings.ini"))
        custom_path = config.get("section_name", "ScriptsDir")
        if custom_path:
            return custom_path
        else:
            return os.path.join(
                self.csc_dir, "resources", "scripts", "python", "commands"
            )

    def start_cascadeur(self) -> None:
        csc_path = self.csc_exe_path_addon_preference
        subprocess.Popen([csc_path])

    def execute_csc_command(self, command: str) -> None:
        subprocess.call([self.csc_exe_path_addon_preference, command])
