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
    client = ClientSocket()
    settings_dict = client.receive_message()
    fbx_scene_loader.set_settings(set_export_settings(settings_dict))
    fbx_scene_loader.export_all_objects(export_path)
    scene.info(f"File exported to {export_path}")

    client.send_message(export_path)
    client.close()


def set_export_settings(preferences: dict = {}) -> csc.fbx.FbxSettings:
    settings = csc.fbx.FbxSettings()
    settings.mode = csc.fbx.FbxSettingsMode.Binary

    if preferences.get("selected_interval"):
        settings.export_selected_interval = True
    else:
        settings.export_selected_interval = False
    if preferences.get("euler_filter"):
        settings.apply_euler_filter = True
    else:
        settings.apply_euler_filter = False
    if preferences.get("up_axis") == "Z":
        settings.up_axis = csc.fbx.FbxSettingsAxis.Z
    else:
        settings.up_axis = csc.fbx.FbxSettingsAxis.Y
    if not preferences.get("bake_animation"):
        settings.bake_animation = False
    else:
        settings.bake_animation = True
    return settings


def get_export_path() -> str:
    temp_dir = tempfile.gettempdir()
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return os.path.join(temp_dir, f"temp_export_{current_time}.fbx")
