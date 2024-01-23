import os
import time
import tempfile
import shutil
from typing import List


def file_exists(file_path: str) -> bool:
    """
    Checking if file exists.

    :param str file_path: Path of the file.
    :return bool: True if the file exsits otherwise False
    """
    return os.path.exists(file_path)


def delete_file(file_path: str) -> None:
    """
    Delete the file from the provided path.

    :param str file_path: Path of the file
    """
    if file_exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")


def get_export_path() -> str:
    """
    Export path of the fbx file in the tempfile directory.
    Filename is based on current time.

    :return str: Desired export path of the fbx file
    """
    temp_dir = tempfile.gettempdir()
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return os.path.join(temp_dir, f"temp_export_{current_time}.fbx")


def copy_files(
    source_folder: str, target_folder: str, file_list: List[str], overwrite: bool = True
) -> bool:
    """
    Coping list of files from the source_folder to the target_folder.

    :param str source_folder: Folder where the files are located
    :param str target_folder: Folder where the files will be copied
    :param List[str] file_list: List of files to be compied
    :param bool overwrite: Overwrite existing files, defaults to True
    :return bool: Returns True if no PermissionError is raised
    """
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
