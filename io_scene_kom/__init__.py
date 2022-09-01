# Copyright (c) 2022 Im Yongsik


# The bl_info is a meta field used by Blender to describe this add-on.
bl_info = {
    "name": "Kepler Object Model Format",
    "author": "Im Yongsik",
    "version": (0, 0, 1),
    "blender": (3, 22, 0),
    "location": "File > Export > Kepler Object Model(.kom)",
    "description": "Export model shading data, like vertices, UVs, normals, etc.",
    "category": "Import-Export",
}

from .import_kom import *
from .export_kom import *

import bpy
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import StringProperty
from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatProperty,
    EnumProperty,
)
from bpy_extras.io_utils import (
    ImportHelper,
    ExportHelper,
    orientation_helper,
    path_reference_mode,
    axis_conversion,
)


@orientation_helper(axis_forward="Z", axis_up="Y")
class ImportKom(bpy.types.Operator, ImportHelper):
    """Load a .kom File"""

    bl_idname = "import_model.kom"
    bl_label = "Import kom"
    bl_options = {"UNDO", "PRESET"}

    directory: StringProperty()

    filename_ext = ".kom"
    filter_glob: StringProperty(default="*.kom", options={"HIDDEN"})

    def draw(self, context):
        layout = self.layout

    def execute(self, context):
        return ImportFile(self.filepath)


@orientation_helper(axis_forward="Z", axis_up="Y")
class ExportKom(bpy.types.Operator, ExportHelper):
    """Write a .kom File"""

    bl_idname = "export_model.kom"
    bl_label = "Export kom"
    bl_options = {"UNDO", "PRESET"}

    filename_ext = ".kom"
    filter_glob: StringProperty(default="*.kom", options={"HIDDEN"})

    def draw(self, context):
        layout = self.layout

    @property
    def check_extension(self):
        return True

    def execute(self, context):
        return ExportFile(self.filepath)


def menu_func_import(self, context):
    self.layout.operator(ImportKom.bl_idname, text="Kepler Object Model (.kom)")


def menu_func_export(self, context):
    self.layout.operator(ExportKom.bl_idname, text="Kepler Object Model (.kom)")


classes = (ImportKom, ExportKom)


def register():
    print("Registering plugin: Kepler Model Exporter")
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    print("Removing plugin: Kepler Model Exporter")
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
