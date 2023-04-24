import csc

import tempfile
import time
import os

from .client_socket import ClientSocket


def command_name():
    return "External commands.Temp Exporter"


def get_export_path():
    temp_dir = tempfile.gettempdir()
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return os.path.join(temp_dir, f"temp_export_{current_time}.fbx")


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
    # https://cascadeur.com/python-api/csc.html#csc.fbx.FbxSettings
    # https://cascadeur.com/python-api/csc.html#csc.fbx.FbxLoader
    fbx_scene_loader.export_all_objects(export_path)
    scene.info(f"File exported to {export_path}")
    client = ClientSocket()
    client.send_message(export_path)
    client.close()


def save_func(file_name):
    mp = csc.app.get_application()
    settings = csc.fbx.FbxSettings()
    settings.mode = csc.fbx.FbxSettingsMode.Ascii
    settings.export_selected_interval = True
    settings.apply_euler_filter = False
    settings.up_axis = csc.fbx.FbxSettingsAxis.Y

    scene_pr = mp.get_scene_manager().current_scene()
    fbx_scene_loader = (
        csc.app.get_application()
        .get_tools_manager()
        .get_tool("FbxSceneLoader")
        .get_fbx_loader(scene_pr)
    )
    fbx_scene_loader.set_settings(settings)
    fbx_scene_loader.export_joints(file_name)
    mp.get_action_manager().call_action("Scene.Undo")
