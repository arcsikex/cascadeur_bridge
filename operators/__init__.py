if "bpy" not in locals():
    from . import fbx_transfer
else:
    import importlib

    importlib.reload(fbx_transfer)

classes = [
    fbx_transfer.CBB_OT_import_cascadeur_fbx,
    fbx_transfer.CBB_OT_import_action_to_selected,
    fbx_transfer.CBB_OT_start_cascadeur,
]
