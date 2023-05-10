import bpy


class CBB_PG_operator_settings(bpy.types.PropertyGroup):
    ns_sort_collections_abc: bpy.props.BoolProperty(
        name="Sort collections alphabetically",
        description="Sort the collections in the outliner alphabetically when stars are generated",
        default=True,
    )
