import os
import time


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
