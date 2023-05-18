if "bpy" not in locals():
    from . import main_panel
    from . import socials
    from . import settings_panel
else:
    import importlib

    importlib.reload(main_panel)
    importlib.reload(socials)
    importlib.reload(settings_panel)

import bpy

classes = [
    main_panel.CBB_PT_parent_panel,
    settings_panel.CBB_PT_csc_bridge_settings,
    settings_panel.CBB_PT_csc_export_settings,
    settings_panel.CBB_PT_blender_import_settings,
    settings_panel.CBB_PT_blender_export_settings,
    socials.CBB_PT_csc_bridge_info,
]
