if "bpy" not in locals():
    from . import reciever
else:
    import importlib

    importlib.reload(reciever)

import bpy

classes = [reciever.CT_OT_get_animamtion_from_cascadeur]
