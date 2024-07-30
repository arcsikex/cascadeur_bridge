import csc


def command_name():
    return "External commands.Temp Importer"


def run(scene):
    from .client_socket import ClientSocket

    mp = csc.app.get_application()
    scene_pr = mp.get_scene_manager().current_scene()
    fbx_scene_loader = (
        csc.app.get_application()
        .get_tools_manager()
        .get_tool("FbxSceneLoader")
        .get_fbx_loader(scene_pr)
    )

    try:
        client = ClientSocket()
    except Exception as e:
        scene.error(f"Couldn't create socket. Error: {e}")
        return
    message: dict = client.receive_message()
    file_path = message.get("file_path")

    import_method = getattr(fbx_scene_loader, message.get("import_method"))
    import_method(file_path)
    scene.info(f"File imported from {file_path}")
    client.send_message("SUCCESS")
    client.close()
