#-----------------------------------------------------#  
#
#    Copyright (c) 2022 Blake Darrow <contact@blakedarrow.com>
#
#    See the LICENSE file for your full rights.
#
#-----------------------------------------------------#  
#   Imports
#-----------------------------------------------------# 
import bpy
import math
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       )
#-----------------------------------------------------#         
#     handles ui panel 
#-----------------------------------------------------#  

class DarrowToolPanel:
    bl_category = "DarrowToolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

class DARROW_PT_toolPanel(DarrowToolPanel, bpy.types.Panel):
    bl_label = "Modeling Tools"
    bl_category = "DarrowToolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "DARROW_PT_toolPanel"

    def draw_header(self, context):
        settings = context.preferences.addons[__package__].preferences
        self.layout.prop(settings, 'advancedCircleBool',
                         icon="SETTINGS", text="")
        Var_displayBool = bpy.context.scene.vertexDisplayBool
        Var_viewportShading = bpy.context.space_data.shading.type
     
        if Var_displayBool ==True:
            self.layout.operator('set.display', icon="HIDE_OFF",
                                 text="", depress=Var_displayBool)
        else:
            self.layout.operator('set.display', icon="HIDE_ON",
                                text="", depress=Var_displayBool)
        if Var_viewportShading != 'SOLID':
            self.layout.enabled = False
    
    def draw(self, context):
        layout = self.layout
        objs = context.selected_objects
        all = bpy.data.objects
        if len(all) != 0:
            obj = context.active_object

            if context.mode == 'EDIT_MESH':
                split = layout.box()
                col = split.column(align=True)
                col.scale_y = 1.33
                col.operator('set.origin', icon="PIVOT_CURSOR")

            if context.mode == 'OBJECT':
                split = layout.box()
                col = split.column(align=True)
                col.scale_y = 1.33
                col.operator('move.origin', icon="OBJECT_ORIGIN")
                col.operator('clean.mesh', text = "Cleanup Mesh", icon="VERTEXSEL")
                col.operator('shade.smooth', text = "Shade Smooth",icon="MOD_SMOOTH")
                col.operator('apply.transforms', icon="CHECKMARK")
                col.operator('apply.normals', icon="NORMALS_FACE")

                if len(objs) == 0:
                    col.enabled = False

                else:
                    col.enabled = True

class DARROW_PT_toolPanel_2(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolPanel"
    bl_label = "Circular Array"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        all = bpy.data.objects
        if len(all) != 0:
            settings = context.preferences.addons[__package__].preferences
            Var_advancedBool = settings.advancedCircleBool
            layout = self.layout
            objs = context.selected_objects
            xAxis = settings.xBool
            yAxis = settings.yBool
            zAxis = settings.zBool
            col = layout.column(align=True)

            col.scale_y = 1.33
            col.prop(context.scene, 'arrayAmount', slider=True)

            col = layout.column(align=True)
            col.scale_y = 1.5
            col.operator('circle.array', icon="ONIONSKIN_ON",)
            if xAxis == False and yAxis == False and zAxis == False:
                col.enabled = False
            elif len(objs) != 0:
                col.enabled = True
            else:
                col.enabled = False
            col.separator()

            col = layout.column(align=True)

            col.label(text="Orientation")
            row = layout.row(align=True)
            split = row.split(align=True)
            split.prop(settings, 'xBool', toggle=True)

            if yAxis == True:
                split.enabled = False
            if zAxis == True:
                split.enabled = False

            split = row.split(align=True)
            split.prop(settings, 'yBool', toggle=True)
            if xAxis == True:
                split.enabled = False
            if zAxis == True:
                split.enabled = False

            split = row.split(align=True)
            split.prop(settings, 'zBool', toggle=True)
            if xAxis == True:
                split.enabled = False
            if yAxis == True:
                split.enabled = False

            col = layout.row(align=True)
            col.scale_y = 1.2
            
            col.operator('view.create_orient', text="Set")
            col.operator('clear.orientation', text="Clear")

            if Var_advancedBool == True:
                box = layout.box()
                col2 = box.column(align=False)
                col2.label(text="Advanced")
                col2.scale_y = 1.2
                col2.operator(
                    'clear.array', text="Delete Array", icon="TRASH")
                if len(objs) == 0:
                    box.enabled = False
                box.prop(settings, 'moveEmptyBool', toggle=False,
                            text="Move empty to 'Empties'")

class DARROW_PT_toolPanel_3(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolPanel"
    bl_label = "RGB Masking"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        all = bpy.data.objects
        if len(all) != 0:
            objs = context.selected_objects
            layout = self.layout
            split = layout.column()
            row = split.row(align=True)
            row.scale_y = 1.1
            row.operator('set.black')
            row.operator('set.white')
            if len(objs) == 0:
                row.enabled = False

            row = split.row(align=True)
            row.scale_y = 1.1
            row.operator('set.red')
            row.operator('set.green')
            row.operator('set.blue')
            split = layout.column()
            if len(objs) == 0:
                row.enabled = False

class createOrient(bpy.types.Operator):
    bl_idname = "view.create_orient"
    bl_label = "Set Orientation"
    bl_description = "There is nothing here"
    bl_options = {"UNDO"}

    def execute(self, context):
        bpy.ops.transform.create_orientation(use=True)
        return {'FINISHED'}

class CTO_OT_Dummy(bpy.types.Operator):
    bl_idname = "object.cto_dummy"
    bl_label = ""
    bl_description = "There is nothing here"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return False

    def execute(self, context):
        return {'FINISHED'}

def extend_transfo_pop_up(self, context):
    layout = self.layout
    row = layout.row(align=False)
    row.operator(DarrowClearOrientation.bl_idname, icon='TRASH')
    row.operator(CTO_OT_Dummy.bl_idname, icon='BLANK1', emboss=False)

#-----------------------------------------------------#
#     set Black color
#-----------------------------------------------------#
class DarrowSetBlack(bpy.types.Operator):
    bl_idname = "set.black"
    bl_label = "Black"

    def execute(self, context):
        bpy.data.brushes["Draw"].color = (0, 0, 0)
        DarrowSetColor.execute(self, context)
        return {'FINISHED'}

#-----------------------------------------------------#
#     set White color
#-----------------------------------------------------#
class DarrowSetWhite(bpy.types.Operator):
    bl_idname = "set.white"
    bl_label = "White"

    def execute(self, context):
        bpy.data.brushes["Draw"].color = (1, 1, 1)
        DarrowSetColor.execute(self, context)
        return {'FINISHED'}

#-----------------------------------------------------#
#     set Red color
#-----------------------------------------------------#
class DarrowSetRed(bpy.types.Operator):
    bl_idname = "set.red"
    bl_label = "Red"

    def execute(self, context):
        bpy.data.brushes["Draw"].color = (1, 0, 0)
        DarrowSetColor.execute(self, context)
        return {'FINISHED'}

#-----------------------------------------------------#
#     set Green color
#-----------------------------------------------------#
class DarrowSetGreen(bpy.types.Operator):
    bl_idname = "set.green"
    bl_label = "Green"

    def execute(self, context):
        bpy.data.brushes["Draw"].color = (0, 1, 0)
        DarrowSetColor.execute(self, context)
        return {'FINISHED'}

#-----------------------------------------------------#
#     set Blue color
#-----------------------------------------------------#
class DarrowSetBlue(bpy.types.Operator):
    bl_idname = "set.blue"
    bl_label = "Blue"

    def execute(self, context):
        bpy.data.brushes["Draw"].color = (0, 0, 1)
        DarrowSetColor.execute(self, context)
        return {'FINISHED'}

#-----------------------------------------------------#
#     handles setting vertex color
#-----------------------------------------------------#
class DarrowSetColor(bpy.types.Operator):
    bl_idname = "set.color"
    bl_label = "Set Color"

    def execute(self, context):
        current_mode = bpy.context.object.mode
        if current_mode == 'OBJECT':
            view_layer = bpy.context.view_layer
            obj_active = view_layer.objects.active
            selection = bpy.context.selected_objects
            bpy.ops.object.select_all(action='DESELECT')

            for obj in selection:
                view_layer.objects.active = obj
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.paint.vertex_paint_toggle()
                bpy.ops.paint.vertex_color_set()
                bpy.ops.object.mode_set(mode='OBJECT')
                obj.select_set(True)

        if current_mode == 'EDIT':
            view_layer = bpy.context.view_layer
            obj_active = view_layer.objects.active
            selection = bpy.context.selected_objects

            for obj in selection:
                view_layer.objects.active = obj
                bpy.ops.paint.vertex_paint_toggle()
                bpy.context.object.data.use_paint_mask = True
                bpy.ops.paint.vertex_color_set()
                bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

#-----------------------------------------------------#
#     handles setting shading display
#-----------------------------------------------------#
class DarrowSetDisplay(bpy.types.Operator):
    bl_idname = "set.display"
    bl_name = "Show Color"
    bl_label = "Toggle vertex color visability"
    """
    We have to have this class here to toggle the bool value,
    so that a user can still manualy change the shading method
    """

    def execute(self, context):
        Var_displayBool = bpy.context.scene.vertexDisplayBool
        Var_viewportShading = bpy.context.space_data.shading.type

        # Toggle bool value everytime this operator is called
        Var_displayBool = not Var_displayBool

        if Var_displayBool == True and Var_viewportShading == 'SOLID':
            bpy.context.space_data.shading.color_type = 'VERTEX'
        elif Var_viewportShading == 'SOLID':
            bpy.context.space_data.shading.color_type = 'MATERIAL'

        bpy.context.scene.vertexDisplayBool = Var_displayBool
        return {'FINISHED'}

#-----------------------------------------------------#
#     handles array
#-----------------------------------------------------#
class DarrowCircleArray(bpy.types.Operator):
    bl_idname = "circle.array"
    bl_description = "Move selected to world origin"
    bl_label = "Array Selected"
    bl_options = {"UNDO"}

    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()

        collectionFound = False
        obj = bpy.context.selected_objects[0]
        amt = context.scene.arrayAmount
        settings = context.preferences.addons[__package__].preferences
        selected = bpy.context.selected_objects[0]
        empty_collection_name = "Darrow_Empties"

        for myCol in bpy.data.collections:
            if myCol.name == empty_collection_name:
                collectionFound = True
                break

        if collectionFound == False:
            col = bpy.data.collections.new(empty_collection_name)
            bpy.context.scene.collection.children.link(col)
            try:
                vlayer = bpy.context.scene.view_layers["View Layer"]
            except:
                vlayer = bpy.context.scene.view_layers["ViewLayer"]
            vlayer.layer_collection.children[empty_collection_name].hide_viewport = True
            bpy.data.collections[empty_collection_name].color_tag = 'COLOR_01'

        else:
            col = bpy.data.collections[empty_collection_name]

        bpy.context.scene.cursor.rotation_euler = (0, 0, 0)
        bpy.ops.object.transform_apply(
            location=True, rotation=True, scale=True)
        try:
            if bpy.context.object.modifiers["DarrowToolkitArray"].offset_object == None:
                modifier_to_remove = obj.modifiers.get("DarrowToolkitArray")
                obj.modifiers.remove(modifier_to_remove)
                context.object.linkedEmpty = "tmp"
                print("Resetting modifier")
        except:
            print("No modifier present")

        if context.object.linkedEmpty == "tmp":
            print("Creating array")
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD')
            bpy.context.object.empty_display_size = settings.emptySize
            empty = bpy.context.selected_objects[0]

        else:
            print("Array exists")
            try:
                vlayer = bpy.context.scene.view_layers["View Layer"]
            except:
                vlayer = bpy.context.scene.view_layers["ViewLayer"]
            vlayer.layer_collection.children[empty_collection_name].hide_viewport = False
            bpy.data.collections[empty_collection_name].color_tag = 'COLOR_01'
            empty = bpy.data.objects[context.object.linkedEmpty]

        bpy.ops.object.select_all(action='DESELECT')
        selected.select_set(state=True)
        context.view_layer.objects.active = selected
        context.object.linkedEmpty = empty.name
        array = False
        mod = bpy.context.object

        for modifier in mod.modifiers:
            if modifier.name == "DarrowToolkitArray":
                array = True

        if not array:
            modifier = obj.modifiers.new(
                name='DarrowToolkitArray', type='ARRAY')

            modifier.name = "DarrowToolkitArray"
            modifier.count = amt
            modifier.use_relative_offset = False
            modifier.use_object_offset = True
            modifier.offset_object = empty
        else:
            modifier_to_remove = obj.modifiers.get("DarrowToolkitArray")
            obj.modifiers.remove(modifier_to_remove)

            modifier = obj.modifiers.new(
                name='DarrowToolkitArray', type='ARRAY')

            modifier.name = "DarrowToolkitArray"
            modifier.count = amt
            modifier.use_relative_offset = False
            modifier.use_object_offset = True
            modifier.offset_object = empty

        modAmt = -1
        for mod in (obj.modifiers):
           modAmt = modAmt + 1

        bpy.ops.object.modifier_move_to_index(
            modifier="DarrowToolkitArray", index=modAmt)
        bpy.ops.object.select_all(action='DESELECT')
        empty.select_set(state=True)
        selected.select_set(state=False)
        context.view_layer.objects.active = empty
        bpy.ops.object.transform_apply(
            location=True, rotation=True, scale=True)
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        if settings.xBool == True:
            axis = 'X'
        if settings.yBool == True:
            axis = 'Y'
        if settings.zBool == True:
            axis = 'Z'
        rotation = 360 / amt
        value = math.radians(rotation)
        orient = bpy.data.scenes['Scene'].transform_orientation_slots[0].type
        bpy.ops.transform.rotate(
            value=value, orient_axis=axis, orient_type=orient,)
        bpy.ops.object.select_all(action='DESELECT')
        empty.select_set(state=False)
        selected.select_set(state=True)
        context.view_layer.objects.active = selected
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)

        empty.select_set(state=True)
        selected.select_set(state=True)
        context.view_layer.objects.active = selected

        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        bpy.ops.object.select_all(action='DESELECT')

        if settings.moveEmptyBool == True:
            empty.select_set(state=True)
            context.view_layer.objects.active = empty
            for coll in empty.users_collection:
                coll.objects.unlink(empty)

            col.objects.link(empty)
        else:
            for coll in empty.users_collection:
                coll.objects.unlink(empty)
            context.scene.collection.objects.link(empty)

        try:
            vlayer = bpy.context.scene.view_layers["View Layer"]
        except:
            vlayer = bpy.context.scene.view_layers["ViewLayer"]
        vlayer.layer_collection.children[empty_collection_name].hide_viewport = True
        empty.select_set(state=False)
        selected.select_set(state=True)
        context.view_layer.objects.active = selected

        return {'FINISHED'}

#-----------------------------------------------------#
#     handles array
#-----------------------------------------------------#
class DarrowClearSelected(bpy.types.Operator):
    bl_idname = "clear.array"
    bl_description = "Move selected to world origin"
    bl_label = "Clear Selected"
    bl_options = {"UNDO"}

    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()
        obj = bpy.context.selected_objects[0]
        selected = bpy.context.selected_objects[0]

        if not context.object.linkedEmpty == "tmp":
            empty = bpy.data.objects[context.object.linkedEmpty]
            context.object.linkedEmpty = empty.name
        else:
            context.object.linkedEmpty == "tmp"

        bpy.ops.object.select_all(action='DESELECT')
        selected.select_set(state=True)
        context.view_layer.objects.active = selected

        mod = bpy.context.object

        for modifier in mod.modifiers:
            if modifier.name == "DarrowToolkitArray":
                modifier_to_remove = obj.modifiers.get("DarrowToolkitArray")
                obj.modifiers.remove(modifier_to_remove)

        if not context.object.linkedEmpty == "tmp":
            bpy.ops.object.select_all(action='DESELECT')
            empty.select_set(state=True)
            selected.select_set(state=False)
            context.view_layer.objects.active = empty
            objs = bpy.data.objects
            objs.remove(objs[empty.name], do_unlink=True)

        selected.select_set(state=True)
        context.view_layer.objects.active = selected
        context.object.linkedEmpty = "tmp"

        return {'FINISHED'}

#-----------------------------------------------------#
#     handles Orientation 
#-----------------------------------------------------#
class DarrowClearOrientation(bpy.types.Operator):
    bl_idname = "clear.orientation"
    bl_description = "clear.orientation"
    bl_label = "Cleanup"

    def execute(self, context):
        try:
            bpy.context.scene.transform_orientation_slots[0].type = ""
        except Exception as inst:
            transforms = str(inst).split(
                "in")[1][3:-2].replace("', '", " ").split()
            for type in transforms[6:]:
                try:
                    bpy.context.scene.transform_orientation_slots[0].type = type
                    bpy.ops.transform.delete_orientation()
                except Exception as e:
                    pass
        return {'FINISHED'}
  
#-----------------------------------------------------#  
#    handles mesh clean up
#-----------------------------------------------------#  
class DarrowCleanMesh(bpy.types.Operator):
    bl_idname = "clean.mesh"
    bl_description = "Delete loose, remove doubles, and dissolve degenerate"
    bl_label = "Clean Mesh"

    def execute(self, context):
        settings = context.preferences.addons[__package__].preferences
        objs = context.selected_objects
        if len(objs) != 0: 
            if context.mode == 'OBJECT':
                bpy.ops.object.editmode_toggle()

            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.delete_loose()
            bpy.ops.mesh.remove_doubles(threshold=settings.removeDoublesAmount)
            bpy.ops.mesh.dissolve_degenerate()
            bpy.ops.object.editmode_toggle()   
            self.report({'INFO'}, "Mesh cleaned")
        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}

#-----------------------------------------------------#  
#    handle apply transforms
#-----------------------------------------------------#  
class DarrowTransforms(bpy.types.Operator):
    bl_idname = "apply.transforms"
    bl_description = "Apply transformations to selected object"
    bl_label = "Apply Transforms"
    bl_options = {"UNDO"}

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) != 0: 
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=True)
            bpy.ops.object.transform_apply(location=True,rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            self.report({'INFO'}, "Transforms applied")
        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}

#-----------------------------------------------------#  
#    handles Objects origin
#-----------------------------------------------------#  
class DarrowSetOrigin(bpy.types.Operator):
    bl_idname = "set.origin"
    bl_description = "Set selected as object origin"
    bl_label = "Set Origin"

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) != 0: 
            if context.mode == 'OBJECT':
                bpy.ops.object.editmode_toggle()
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            self.report({'INFO'}, "Selected is now origin")
        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}

#-----------------------------------------------------#  
#     handles snapping object to world center
#-----------------------------------------------------#   
class DarrowMoveOrigin(bpy.types.Operator):
    bl_idname = "move.origin"
    bl_description = "Move selected to world origin"
    bl_label = "Move to Origin"

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) != 0: 
            bpy.ops.view3d.snap_cursor_to_center()
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
            self.report({'INFO'}, "Moved selected to object origin")
        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}

#-----------------------------------------------------#  
#     handles apply outside calculated normals
#-----------------------------------------------------#    
class DarrowNormals(bpy.types.Operator):
    bl_idname = "apply.normals"
    bl_description = "Calculate outside normals"
    bl_label = "Calculate Normals"

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) != 0: 
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.editmode_toggle()
            self.report({'INFO'}, "Normals calculated outside")
        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}
    
#-----------------------------------------------------#  
#     handles smooth mesh
#-----------------------------------------------------#    
class DarrowSmooth(bpy.types.Operator):
    bl_idname = "shade.smooth"
    bl_label = "Smooth Object"
    bl_description = "Smooth the selected object"

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) != 0: 
            bpy.ops.object.shade_smooth()
            bpy.context.object.data.use_auto_smooth = True
            bpy.context.object.data.auto_smooth_angle = 3.14159

            self.report({'INFO'}, "Object smoothed to 180")
        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}

#-----------------------------------------------------#  
#   Registration classes
#-----------------------------------------------------#
classes = (createOrient,DARROW_PT_toolPanel,  DARROW_PT_toolPanel_2, DARROW_PT_toolPanel_3, CTO_OT_Dummy, DarrowClearOrientation, DarrowCleanMesh, DarrowSetOrigin, DarrowMoveOrigin, DarrowTransforms, DarrowNormals, DarrowSmooth,
           DarrowCircleArray, DarrowClearSelected, DarrowSetBlack, DarrowSetWhite, DarrowSetRed, DarrowSetGreen, DarrowSetBlue, DarrowSetColor, DarrowSetDisplay,)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.vertexDisplayBool = bpy.props.BoolProperty(
        name="",
        description="Toggle visabilty of vertex color",
        default=False
    )

    bpy.types.Scene.parentcoll_string = bpy.props.StringProperty(
            name="Name",
            description="Collection Name",
            default="Collection"
        )

    bpy.types.VIEW3D_PT_transform_orientations.append(extend_transfo_pop_up)

    bpy.types.Scene.compactBool = bpy.props.BoolProperty(
    name = "Advanced",
    description = "Toggle Advanced Mode",
    default = False
    )

    bpy.types.Scene.showWireframeBool = bpy.props.BoolProperty(
    name = "Toggle Wireframe",
    description = "Toggle visabilty of wireframe mode",
    default = False
    )

    bpy.types.Object.linkedEmpty = bpy.props.StringProperty(
        default="tmp"
    )

    bpy.types.Scene.arrayAmount = bpy.props.IntProperty(
        name="Amount",
        description="Amount",
        default=5,
        step=1,
        soft_max=30,
        soft_min=1,
    )

def unregister():
    bpy.types.VIEW3D_PT_transform_orientations.remove(extend_transfo_pop_up)
    
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()