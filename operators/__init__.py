if "bpy" not in locals():
    from . import fbx_transfer
    from . import csc_ops
    from . import addon_properties
else:
    import importlib

    importlib.reload(fbx_transfer)
    importlib.reload(csc_ops)
    importlib.reload(addon_properties)

classes = [
    fbx_transfer.CBB_OT_export_blender_fbx,
    fbx_transfer.CBB_OT_import_cascadeur_fbx,
    fbx_transfer.CBB_OT_import_action_to_selected,
    csc_ops.CBB_OT_start_cascadeur,
    csc_ops.CBB_OT_install_required_files,
    addon_properties.CBB_OT_save_fbx_settings,
]
