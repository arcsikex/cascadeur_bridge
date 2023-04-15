import platform
import subprocess

import bpy


def get_default_csc_path():
    default_csc_path = {
        "Windows": r"C:\Program Files\Cascadeur\cascadeur.exe",
    }
    return default_csc_path.get(platform.system(), None)


def execute_csc_command(command: str) -> None:
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons["blender_side"].preferences

    subprocess.call([addon_prefs.csc_exe_path, command])
