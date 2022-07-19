#-----------------------------------------------------#  
#     Plugin information     
#-----------------------------------------------------#  
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty

bl_info = {
    "name": "Modeling Tools",
    "author": "Blake Darrow",
    "version": (1, 1, 8),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > DarrowTools",
    "description": "Custom modeling tools including arrays and aligning on a grid",
    "category": "Tools",
    "doc_url": "https://docs.darrow.tools/en/latest/index.html",
    }
    
#-----------------------------------------------------#  
#     imports    
#-----------------------------------------------------#  
import bpy
import sys
from . import addon_updater_ops
import importlib

if __package__ != "modeling_tools":
    sys.modules["modeling_tools"] = sys.modules[__package__]

modulesNames = ['ModelingTools', ]

@addon_updater_ops.make_annotations
class DarrowAddonPreferences(AddonPreferences):
    bl_idname = __package__

    auto_check_update: BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )

    updater_intrval_months: IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=3,
        min=0
    )
    updater_intrval_days: IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=0,
        min=0,
    )
    updater_intrval_hours: IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes: IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    checklist_moduleBool: BoolProperty(
        name="Modeling Tools",
        default=True
    )

    organizer_moduleBool: BoolProperty(
        name="Organizer Tools",
        default=True
    )

    export_moduleBool: BoolProperty(
        name="FBX Exporter",
        default=True
    )

    library_moduleBool: BoolProperty(
        name="Mesh Library",
        default=True
    )

    array_moduleBool: BoolProperty(
        name="Circular Array",
        default=True
    )

    rgb_moduleBool: BoolProperty(
        name="Vertex Painter",
        default=True
    )


    xBool: BoolProperty(
        name="X",
        description="Toggle X axis",
        default=False
    )
    yBool: BoolProperty(
        name="Y",
        description="Toggle Y axis",
        default=False
    )
    zBool: BoolProperty(
        name="Z",
        description="Toggle Z axis",
        default=True
    )
    emptySize: FloatProperty(
        name="Array Empty Display Size",
        description="Size of arrays' empty",
        default=0.25,
        soft_min=0,
        soft_max=.5
    )

    advancedVertexBool: BoolProperty(
        name="Advanced",
        description="Show advanced options",
        default=False
    )
    advancedCircleBool: BoolProperty(
        name="Advanced",
        description="Show advanced options",
        default=False
    )

    removeDoublesAmount: FloatProperty(
        name="Remove Doubles Amount",
        description="Threshold to Remove Doubles",
        default=0.01,
        soft_min=0,
        soft_max=.25,
        precision=3
    )
    moveEmptyBool: BoolProperty(
        name="Create CircleArray empties under 'Darrow_Empties'.",
        description="Hide empty under object",
        default=True
    )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Module Properties")
        box.alignment = 'RIGHT'
        split = box.split(factor=0.7)
        box.scale_y = 1.1
        col1 = split.column(align=True)

        col1.prop(self, "emptySize", text="Empty Display Size", slider=True)
        col1.prop(self, "removeDoublesAmount",
                  text="Remove Doubles Distance", slider=True)
        col1.prop(self, "moveEmptyBool", text="Move empties to 'Empty Collection'")


        addon_updater_ops.update_settings_ui(self, context)

#-----------------------------------------------------#  
#     create a dictonary for module names    
#-----------------------------------------------------# 
modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

#-----------------------------------------------------#  
#     import new modules to addon using full name from above    
#-----------------------------------------------------# 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)

#-----------------------------------------------------#  
#     register the modules    
#-----------------------------------------------------# 
classes = (DarrowAddonPreferences,)

def register():
    addon_updater_ops.register(bl_info)
    for cls in classes:
        bpy.utils.register_class(cls)
        
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

#-----------------------------------------------------#  
#     unregister the modules    
#-----------------------------------------------------# 
def unregister():
    addon_updater_ops.unregister()
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()

if __name__ == "__main__":
    register()