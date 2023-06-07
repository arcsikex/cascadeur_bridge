import subprocess
import platform
import os

from . import file_handling
import bpy
from ..addon_info import PACKAGE_NAME


class CascadeurHandler:
    required_scripts = [
        "__init__.py",
        "temp_exporter.py",
        "temp_importer.py",
        "client_socket.py",
    ]

    @property
    def csc_exe_path_addon_preference(self) -> str:
        preferences = bpy.context.preferences
        addon_prefs = preferences.addons[PACKAGE_NAME].preferences
        return addon_prefs.csc_exe_path

    @property
    def csc_dir(self) -> str:
        if self.is_csc_exe_path_valid:
            return (
                self.csc_exe_path_addon_preference
                if platform.system() == "Darwin"
                else os.path.dirname(self.csc_exe_path_addon_preference)
            )

    @property
    def is_csc_exe_path_valid(self) -> bool:
        csc_path = self.csc_exe_path_addon_preference
        return True if csc_path and file_handling.file_exists(csc_path) else False

    @property
    def commands_path(self) -> str:
        resources_dir = (
            os.path.join(self.csc_dir, "Contents", "MacOS", "resources")
            if platform.system() == "Darwin"
            else os.path.join(self.csc_dir, "resources")
        )
        commands_config = os.path.join(resources_dir, "settings.ini")
        with open(commands_config, "r") as f:
            for line in f:
                if line.startswith("ScriptsDir"):
                    scripts_dir = line.split("=")[1].strip().strip('"')
                    break
        if scripts_dir:
            return scripts_dir
        else:
            return os.path.join(resources_dir, "scripts", "python", "commands")

    def start_cascadeur(self) -> None:
        csc_path = self.csc_exe_path_addon_preference
        subprocess.Popen([csc_path])

    def execute_csc_command(self, command: str) -> None:
        if platform.system() == "Windows":
            subprocess.Popen(
                [self.csc_exe_path_addon_preference, "-run-script", command],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
        else:
            subprocess.Popen(
                [self.csc_exe_path_addon_preference, "-run-script", command]
            )

    @property
    def are_commands_installed(self) -> bool:
        for file in self.required_scripts:
            if not file_handling.file_exists(
                os.path.join(self.commands_path, "externals", file)
            ):
                return False
        return True
