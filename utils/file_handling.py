import os
import time
import tempfile
import shutil


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


def get_export_path():
    temp_dir = tempfile.gettempdir()
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return os.path.join(temp_dir, f"temp_export_{current_time}.fbx")


def copy_files(source_folder, target_folder, file_list, overwrite=True):
    """
    Copy a list of files from a source folder to a target folder.

    Args:
        source_folder (str): The path to the source folder.
        target_folder (str): The path to the target folder.
        file_list (list): A list of file names to be copied.

    Returns:
        None
    """
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    if not os.access(target_folder, os.W_OK):
        print(f"Error: Write access to {target_folder} denied.")
        return False

    for file_name in file_list:
        source_path = os.path.join(source_folder, file_name)
        target_path = os.path.join(target_folder, file_name)
        if not overwrite and file_exists(target_path):
            continue
        try:
            shutil.copy2(source_path, target_path)
        except shutil.Error as e:
            print(f"Error copying {source_path} to {target_path}: {e}")
            return False
    return True
