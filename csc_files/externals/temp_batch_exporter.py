import csc

from .client_socket import ClientSocket
from . import commons


def command_name():
    return "External commands.Temp Exporter"


def run(scene):
    scene_manager = csc.app.get_application().get_scene_manager()
    scenes = scene_manager.scenes()
    try:
        client = ClientSocket()
    except Exception as e:
        scene.error(f"Couldn't create socket. Error: {e}")
        return
    settings_dict = client.receive_message()
    export_paths = []

    for s in scenes:
        fbx_scene_loader = (
            csc.app.get_application()
            .get_tools_manager()
            .get_tool("FbxSceneLoader")
            .get_fbx_loader(s)
        )
        export_path = commons.get_export_path(s.name())
        fbx_scene_loader.set_settings(commons.set_export_settings(settings_dict))
        fbx_scene_loader.export_all_objects(export_path)
        export_paths.append(export_path)
        scene.info(f"File exported to {export_path}")

    client.send_message(export_paths)
    client.close()
