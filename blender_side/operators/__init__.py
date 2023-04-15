if "bpy" not in locals():
    from . import fbx_transfer
    from . import reciever
else:
    import importlib

    importlib.reload(fbx_transfer)
    importlib.reload(reciever)

import bpy

classes = [reciever.CT_OT_start_server, fbx_transfer.CT_OT_import_cascadeur_fbx]
