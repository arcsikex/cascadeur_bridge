import os
import configparser

config_path = os.path.join(os.path.dirname(__file__), "..", "settings.cfg")


def _get_parser():
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def get_panel_name():
    config = _get_parser()
    return config.get("Addon Settings", "panelname", fallback="CSC Bridge")


def set_panel_name(new_name):
    config = _get_parser()
    config.set("Addon Settings", "panelname", new_name)
    with open(config_path, "w") as configfile:
        config.write(configfile)
