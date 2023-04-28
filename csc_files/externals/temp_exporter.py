import csc

import tempfile
import time
import os

from .client_socket import ClientSocket


def command_name():
    return "External commands.Temp Exporter"


def run(scene):
    mp = csc.app.get_application()
    scene_pr = mp.get_scene_manager().current_scene()
    fbx_scene_loader = (
        csc.app.get_application()
        .get_tools_manager()
        .get_tool("FbxSceneLoader")
        .get_fbx_loader(scene_pr)
    )
    export_path = get_export_path()
    fbx_scene_loader.set_settings(set_export_settings())
    fbx_scene_loader.export_all_objects(export_path)
    scene.info(f"File exported to {export_path}")
    client = ClientSocket()
    client.send_message(export_path)
    client.close()


def set_export_settings(preferences: dict = {}) -> csc.fbx.FbxSettings:
    settings = csc.fbx.FbxSettings()
    if preferences.get("mode") == "Ascii":
        settings.mode = csc.fbx.FbxSettingsMode.Ascii
    else:
        settings.mode = csc.fbx.FbxSettingsMode.Binary
    if preferences.get("selected_interval"):
        settings.export_selected_interval = True
    else:
        settings.export_selected_interval = False
    if preferences.get("euler_filter"):
        settings.apply_euler_filter = True
    else:
        settings.apply_euler_filter = True
    if preferences.get("up_axis") == "Z":
        settings.up_axis = csc.fbx.FbxSettingsAxis.Z
    else:
        settings.up_axis = csc.fbx.FbxSettingsAxis.Y
    return settings


def get_export_path() -> str:
    temp_dir = tempfile.gettempdir()
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return os.path.join(temp_dir, f"temp_export_{current_time}.fbx")
