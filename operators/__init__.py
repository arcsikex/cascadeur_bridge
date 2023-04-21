if "bpy" not in locals():
    from . import fbx_transfer
    from . import reciever
else:
    import importlib

    importlib.reload(fbx_transfer)
    importlib.reload(reciever)

classes = [
    reciever.CBB_OT_start_server,
    fbx_transfer.CBB_OT_import_cascadeur_fbx,
    fbx_transfer.CBB_OT_import_action_to_selected,
    fbx_transfer.CBB_OT_start_cascadeur,
]
