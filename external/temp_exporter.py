import csc

import tempfile
import socket
import time
import os


def command_name():
    return "Xternal commands.Temp Exporter"


def get_export_path():
    temp_dir = tempfile.gettempdir()
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return os.path.join(temp_dir, f"temp_export_{current_time}.fbx")


def send_file_path(message):
    server_address = ("localhost", 12345)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    attempts = 0
    while True:
        try:
            client_socket.connect(server_address)
            break
        except ConnectionRefusedError:
            if attempts < 10:
                attempts += 1
                time.sleep(0.1)
            else:
                raise
    client_socket.sendall(message.encode())
    response = client_socket.recv(1024)
    print(response.decode())
    client_socket.close()


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
    fbx_scene_loader.export_all_objects(export_path)
    scene.info(f"File exported to {export_path}")
    send_file_path(export_path)
