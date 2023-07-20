import bpy

import os
import configparser

config_path = os.path.join(os.path.dirname(__file__), "..", "settings.cfg")


def get_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def get_config_parameter(
    section: str,
    parameter: str,
    fallback,
    config: configparser.ConfigParser = get_config(),
):
    return config.get(section, parameter, fallback=fallback)


def get_bool_config_parameter(
    section: str,
    parameter: str,
    fallback,
    config: configparser.ConfigParser = get_config(),
):
    return config.getboolean(section, parameter, fallback=fallback)


def set_config_parameter(
    section: str,
    parameter: str,
    value: str,
    config: configparser.ConfigParser = get_config(),
):
    config.set(section, parameter, value)
    with open(config_path, "w") as configfile:
        config.write(configfile)


def get_panel_name():
    return get_config_parameter("Addon Settings", "panel_name", fallback="CSC Bridge")


def save_fbx_settings():
    config = get_config()
    section = "FBX Settings"
    if not config.has_section(section):
        config.add_section(section)

    my_group = bpy.context.scene.cbb_fbx_settings

    for attr_name, attr_value in my_group.rna_type.properties.items():
        if attr_name not in ["rna_type", "name"]:
            print(f"Property: {attr_name}, Value: {getattr(my_group, attr_name)}")
            config.set(section, attr_name, str(getattr(my_group, attr_name)))

    with open(config_path, "w") as configfile:
        config.write(configfile)
