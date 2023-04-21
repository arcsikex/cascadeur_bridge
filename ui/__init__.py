if "bpy" not in locals():
    from . import main_panel
    from . import socials
else:
    import importlib

    importlib.reload(main_panel)
    importlib.reload(socials)

import bpy

classes = [
    main_panel.CBB_PT_parent_panel,
    main_panel.CBB_PT_csc_to_blender,
    socials.CBB_PT_csc_bridge_info,
]
