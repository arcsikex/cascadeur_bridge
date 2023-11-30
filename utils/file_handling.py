import os
import time
import tempfile
import shutil
from typing import List


def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)


def delete_file(file_path: str) -> None:
    if file_exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")


def get_export_path() -> str:
    temp_dir = tempfile.gettempdir()
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return os.path.join(temp_dir, f"temp_export_{current_time}.fbx")


def copy_files(
    source_folder: str, target_folder: str, file_list: List[str], overwrite: bool = True
) -> bool:
    if not os.path.exists(target_folder):
        try:
            os.makedirs(target_folder)
        except PermissionError as e:
            print(f"Error creating {target_folder}: {e}")
            return False

    for file_name in file_list:
        source_path = os.path.join(source_folder, file_name)
        target_path = os.path.join(target_folder, file_name)
        if not overwrite and file_exists(target_path):
            continue
        try:
            shutil.copy2(source_path, target_path)
        except PermissionError as e:
            print(f"Error copying {source_path} to {target_path}: {e}")
            return False
    return True
