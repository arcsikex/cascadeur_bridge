import platform
import subprocess


def get_default_csc_path():
    default_csc_path = {
        "Windows": r"C:\Program Files\Cascadeur\cascadeur.exe",
    }
    return default_csc_path.get(platform.system(), None)


def execut_csc_command(csc_path: str, command: str) -> None:
    subprocess.call([csc_path, command])
