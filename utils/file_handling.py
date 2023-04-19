import os
import time
from .csc_handling import CascadeurHandler


def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path) and os.path.isfile(file_path)


def delete_file(file_path: str) -> None:
    if file_exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")


def wait_for_file(file_path: str, timeout: int = 60) -> bool:
    export_finished = False
    start_time = time.time()

    while not export_finished and time.time() - start_time < timeout:
        if file_exists(file_path):
            export_finished = True
        else:
            time.sleep(1)
    return export_finished


def commands_installed() -> bool:
    _ch = CascadeurHandler()
    base_path = os.path.join(_ch.commands_path, "externals")
    required_files = [
        "__init__.py",
        "temp_exporter.py",
    ]
    for file in required_files:
        full_path = os.path.join(base_path, file)
        if not file_exists(full_path):
            return False
    else:
        return True


def pyds_installed() -> bool:
    _ch = CascadeurHandler()
    base_path = os.path.join(_ch.csc_dir, "python", "DLLs")
    required_files = [
        "_socket.pyd",
        "select.pyd",
    ]
    for file in required_files:
        full_path = os.path.join(base_path, file)
        if not file_exists(full_path):
            return False
    else:
        return True
