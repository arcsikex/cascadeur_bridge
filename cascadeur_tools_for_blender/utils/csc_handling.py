import platform
import subprocess

from . import file_handling

import bpy


def get_default_csc_path():
    default_csc_path = {
        "Windows": r"C:\Program Files\Cascadeur\cascadeur.exe",
    }
    return default_csc_path.get(platform.system(), None)


def get_csc_path_preference() -> str:
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons["cascadeur_tools_for_blender"].preferences
    return addon_prefs.csc_exe_path


def execute_csc_command(command: str) -> None:
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons["cascadeur_tools_for_blender"].preferences

    subprocess.call([addon_prefs.csc_exe_path, command])


def is_csc_path_set() -> bool:
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons["cascadeur_tools_for_blender"].preferences
    csc_path = addon_prefs.csc_exe_path
    return True if csc_path and file_handling.file_exists(csc_path) else False


def start_cascadeur() -> None:
    csc_path = get_csc_path_preference()
    if is_csc_path_set():
        subprocess.Popen([csc_path])
