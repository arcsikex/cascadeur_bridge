if "bpy" not in locals():
    from . import main_panel
    from . import socials
else:
    import importlib

    importlib.reload(main_panel)
    importlib.reload(socials)

import bpy

classes = [
    main_panel.WS_PT_parent_panel,
    main_panel.WS_PT_csc_to_blender,
    socials.WS_PT_csc_tools_info,
]
