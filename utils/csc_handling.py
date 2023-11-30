import subprocess
import platform
import os

from . import file_handling
import bpy
from ..addon_info import PACKAGE_NAME


def get_default_csc_exe_path() -> str:
    """
    Returns the default Cascadeur executable path based on the operating system.

    :return str: Default Cascadeur executable path, or an empty string if not found.
    """
    csc_path = {
        "Windows": r"C:\Program Files\Cascadeur\cascadeur.exe",
        "Linux": r"/opt/cascadeur/cascadeur",
        "Darwin": r"/Applications/Cascadeur.app",
    }
    default = csc_path.get(platform.system(), "")
    return default if file_handling.file_exists(default) else ""


class CascadeurHandler:
    @property
    def csc_exe_path_addon_preference(self) -> str:
        """
        Get the set Cascadeur executable path from the addon's preferences.

        :return str: Cascadeur executable path stored in the addon's preferences.
        """
        preferences = bpy.context.preferences
        addon_prefs = preferences.addons[PACKAGE_NAME].preferences
        return addon_prefs.csc_exe_path

    @property
    def csc_dir(self) -> str:
        """
        Get the root directory of Cascadeur installation.

        :return str: Directory path as a string.
        """
        if self.is_csc_exe_path_valid:
            return (
                self.csc_exe_path_addon_preference
                if platform.system() == "Darwin"
                else os.path.dirname(self.csc_exe_path_addon_preference)
            )

    @property
    def is_csc_exe_path_valid(self) -> bool:
        """
        Check if the Cascadeur executable path is valid.

        :return bool: True if file exists, False otherwise.
        """
        csc_path = self.csc_exe_path_addon_preference
        return True if csc_path and file_handling.file_exists(csc_path) else False

    @property
    def commands_path(self) -> str:
        """
        Get the path to the Cascadeur commands directory.

        :return str: Directory path as a string.
        """
        resources_dir = (
            os.path.join(self.csc_dir, "Contents", "MacOS", "resources")
            if platform.system() == "Darwin"
            else os.path.join(self.csc_dir, "resources")
        )
        return os.path.join(resources_dir, "scripts", "python", "commands")

    def start_cascadeur(self) -> None:
        """
        Start Cascadeur using the specified executable path.

        :return: None
        """
        csc_path = self.csc_exe_path_addon_preference
        subprocess.Popen([csc_path])

    def execute_csc_command(self, command: str) -> None:
        """
        Execute a Cascadeur command using the specified executable path.

        :param command str: Cascadeur command to execute.
        :return: None
        """
        subprocess.Popen([self.csc_exe_path_addon_preference, "--run-script", command])
