import csc


def command_name():
    return "External commands.Temp Exporter"


def run(scene):
    from .client_socket import ClientSocket
    from . import commons

    mp = csc.app.get_application()
    scene_pr = mp.get_scene_manager().current_scene()
    fbx_scene_loader = (
        csc.app.get_application()
        .get_tools_manager()
        .get_tool("FbxSceneLoader")
        .get_fbx_loader(scene_pr)
    )
    export_path = commons.get_export_path(scene_pr.name())
    try:
        client = ClientSocket()
    except Exception as e:
        scene.error(f"Couldn't create socket. Error: {e}")
        return

    settings_dict = client.receive_message()
    fbx_scene_loader.set_settings(commons.set_export_settings(settings_dict))
    fbx_scene_loader.export_all_objects(export_path)
    scene.info(f"File exported to {export_path}")
    client.send_message([export_path])
    client.close()
