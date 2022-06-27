# ##### BEGIN GPL LICENSE BLOCK #####
#
#   Copyright (C) 2022  Blake Darrow <contact@blakedarrow.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

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
    bl_category = "DarrowTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "DARROW_PT_toolPanel"

    #def draw_header(self, context):
        #self.layout.label(text="", icon="MESH_DATA")
    
    def draw(self, context):
        layout = self.layout
        objs = context.selected_objects
        all = bpy.data.objects
        if len(all) != 0:
            if context.mode == 'EDIT_MESH':
                layout = self.layout
                layout.label(text="Mesh Tools")
                col = layout.box().column(align=True)
                col.scale_y = 1.33
                col.operator('set.origin', text="Set as Origin", icon="PIVOT_CURSOR")

            if context.mode == 'OBJECT':
                col = layout.column(align=True)
                col.scale_y = 1
                col.label(text="Mesh Tools")
                cf = layout.box().column_flow(columns=2, align=True)
                cf.scale_y = 1.2
                cf.operator('move.origin', text="Origin",
                            icon="TRANSFORM_ORIGINS")
                cf.operator('cleanup.mesh', text = "Cleanup", icon="VERTEXSEL")
                cf.operator('shade.smooth', text = "Smooth",icon="MOD_SMOOTH")
                cf.operator("unwrap.selected", text="Unwrap", icon="UV")
                cf.operator('apply.transforms', text="Transforms",
                            icon="OBJECT_ORIGIN")
                cf.operator('apply.normals', text="Normals", icon="ORIENTATION_NORMAL")
                cf.operator('shade.sharp', text="Sharp", icon="MOD_NOISE")

                if len(objs) == 0:
                    cf.enabled = False
                else:
                    cf.enabled = True

class DARROW_PT_toolExtendPanel(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolPanel"
    bl_label = "More Tools"
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    def draw(self, context):
        none = None


class DARROW_PT_toolPanel_2(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolExtendPanel"
    bl_label = "Transform Orientations"
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    def draw(self, context):
        layout = self.layout
        cf2 = layout.column_flow(columns=2, align=True)
        cf2.scale_y = 1.33

        cf2.operator('view.create_orient', text="Set", icon="RESTRICT_SELECT_OFF")
        cf2.operator('clear.orientation', text="Clear", icon="TRASH")

class DARROW_PT_toolPanel_3(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolExtendPanel"
    bl_label = "Circular Array"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        all = bpy.data.objects
        if len(all) != 0:
            settings = context.preferences.addons[__package__].preferences
            layout = self.layout
            objs = context.selected_objects
            xAxis = settings.xBool
            yAxis = settings.yBool
            zAxis = settings.zBool
            col = layout.column(align=True)
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
            col.scale_y = 1.33
            col.prop(context.scene, 'arrayAmount', slider=True)

            col = layout.column(align=True)
            col.scale_y = 1.5
            col.operator('circle.array', icon="ONIONSKIN_ON",)
            col.operator(
                'clear.array', text="Remove Array", icon="TRASH")
        
            if xAxis == False and yAxis == False and zAxis == False:
                col.enabled = False
            elif len(objs) != 0:
                col.enabled = True
            else:
                col.enabled = False
                
            if context.mode != 'OBJECT':
                col.enabled = False
           
class DARROW_PT_toolPanel_4(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolExtendPanel"
    bl_label = "Cleanup Mesh"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        all = bpy.data.objects
        objs = context.selected_objects
        if len(all) != 0:
            settings = context.preferences.addons[__package__].preferences
            layout = self.layout
            scn = context.scene
            col = layout.column(align=False)
            col.scale_y = 1.33
            col.prop(settings, "removeDoublesAmount", text="Merge Distance",slider=True)
            col = layout.column(align=True)
            col.scale_y = 1.33
            col.operator("cleanup.mesh", text="Cleanup", icon= "VERTEXSEL")
            col.prop(scn, "fixNgons", text="Fix Ngons", toggle=True, icon="MOD_DECIM")
            if len(objs) == 0:
                col.enabled = False

class DARROW_PT_toolPanel_5(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolExtendPanel"
    bl_label = "RGB Masking"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        all = bpy.data.objects
        if len(all) != 0:
            Var_displayBool = bpy.context.scene.vertexDisplayBool
            Var_viewportShading = bpy.context.space_data.shading.type
            objs = context.selected_objects
            layout = self.layout    
            split = layout.column()
            row = split.row(align=True)
            col = layout.column()
            col.scale_y = 1.33
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

            if Var_displayBool == True:
                col.operator('set.display', icon="HIDE_OFF",
                                     text="Display Color", depress=Var_displayBool)
            else:
                col.operator('set.display', icon="HIDE_ON",
                                     text="Display Color", depress=Var_displayBool)
            if Var_viewportShading != 'SOLID':
                col.enabled = False

class DARROW_PT_toolPanel_6(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolExtendPanel"
    bl_label = "Quick Unwrap"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        all = bpy.data.objects
        if len(all) != 0:
            layout = self.layout
            scn = context.scene
            col = layout.column(align=True)
            col.scale_y = 1.2
            col.operator("unwrap.selected", text="Unwrap All Selection", icon="UV")
            col.prop(scn, "unwrapFloat", text="Angle")

#-----------------------------------------------------#
#    Cleanup Mesh
#-----------------------------------------------------#
class DarrowCleanupMesh(bpy.types.Operator):
    bl_label = "Example"
    bl_idname = "cleanup.mesh"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Attempt to clean mesh"

    def execute(self, context):
        objs = bpy.context.selected_objects
        settings = context.preferences.addons[__package__].preferences

        if len(objs) == 1:
            if context.mode != "EDIT_MESH":
                    bpy.ops.object.editmode_toggle()
            DarrowCleanupMesh.cleanVertices(self,context) # Call other function within this same class
            bpy.ops.object.editmode_toggle()
            self.report({'INFO'}, "Cleaned selected mesh")
            
        elif len(objs) > 1:
            self.report({'ERROR'}, "Please select only one mesh")
    
        elif len(objs) == 0:
            self.report({'ERROR'}, "Please select a mesh")
           
        return {'FINISHED'}
    
    def cleanVertices(self,context):
        settings = context.preferences.addons[__package__].preferences
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.mesh.remove_doubles(threshold= settings.removeDoublesAmount)
        if bpy.context.scene.fixNgons == True:
            DarrowCleanupMesh.cleanNgons()
        bpy.ops.mesh.delete_loose()
         
    def cleanNgons():
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        bpy.ops.mesh.tris_convert_to_quads()

class createOrient(bpy.types.Operator):
    bl_idname = "view.create_orient"
    bl_label = "Set Orientation"
    bl_description = "Set as custom transform orientation"
    bl_options = {"UNDO"}

    def execute(self, context):
        if bpy.context.active_object != None:
            bpy.ops.transform.create_orientation(use=True)
        else:
            self.report({'WARNING'},"Selection cannot be empty")
        return {'FINISHED'}

class CTO_OT_Dummy(bpy.types.Operator):
    bl_idname = "object.cto_dummy"
    bl_label = ""
    bl_description = "Remove custom orientations"
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
    bl_description = "Remove custom orientations"
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
#    handle apply transforms
#-----------------------------------------------------#  
class DarrowTransforms(bpy.types.Operator):
    bl_idname = "apply.transforms"
    bl_description = "Apply transformations to selected object"
    bl_label = "Apply Rot & Scale"
    bl_options = {"UNDO"}

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) != 0: 
            bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=True)
            bpy.ops.object.transform_apply(location=False,rotation=True, scale=True)
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

class DarrowSharp(bpy.types.Operator):
    bl_idname = "shade.sharp"
    bl_label = "Sharpen Object"
    bl_description = "Sharpen the selected object"

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) != 0:
            bpy.ops.object.shade_smooth()
            bpy.context.object.data.use_auto_smooth = True
            bpy.context.object.data.auto_smooth_angle = 1.15192

            self.report({'INFO'}, "Object smoothed to 66")
        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}

#-----------------------------------------------------#
#    Quick Unwrap
#-----------------------------------------------------#
class DarrowUnwrapSelected(bpy.types.Operator):
    bl_label = "Example"
    bl_idname = "unwrap.selected"
    bl_description = "Unwrap all selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = bpy.data.objects
        selection = bpy.context.selected_objects
        active_object = bpy.context.active_object
        angle = math.radians(bpy.context.scene.unwrapFloat)
        
        if context.mode == 'OBJECT':
            bpy.ops.object.select_all(action='DESELECT')
        else:
            bpy.ops.mesh.select_all(action='DESELECT')
        
        for i in selection:
            i.select_set(True)
            bpy.context.view_layer.objects.active = i
            
            if context.mode == 'OBJECT':
                bpy.ops.object.editmode_toggle()
            
            bpy.ops.mesh.select_all(action='SELECT')
            
            bpy.ops.uv.smart_project(
                angle_limit=angle,
                island_margin=0.0, 
                area_weight=0.0, 
                correct_aspect=True,
                scale_to_bounds=False)
                
            bpy.ops.object.editmode_toggle()
            
            i.select_set(False)
                
        amt = len(selection)
        for i in selection:
            i.select_set(True)
        self.report({'INFO'}, "Unwrapped " + str(amt) + " at " + str(bpy.context.scene.unwrapFloat) + " angle")
        return {'FINISHED'}
#-----------------------------------------------------#  
#   Registration classes
#-----------------------------------------------------#
classes = ( DarrowCleanupMesh,DarrowSharp,createOrient,DARROW_PT_toolPanel,DARROW_PT_toolExtendPanel, DARROW_PT_toolPanel_2, DARROW_PT_toolPanel_3, DARROW_PT_toolPanel_4,DARROW_PT_toolPanel_5, DARROW_PT_toolPanel_6, CTO_OT_Dummy, DarrowClearOrientation, DarrowSetOrigin, DarrowMoveOrigin, DarrowTransforms, DarrowNormals, DarrowSmooth,
           DarrowCircleArray, DarrowClearSelected, DarrowSetBlack, DarrowSetWhite, DarrowSetRed, DarrowSetGreen, DarrowSetBlue, DarrowSetColor, DarrowSetDisplay,DarrowUnwrapSelected)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.unwrapFloat = bpy.props.FloatProperty(
        name = "Int",
        default = 66,
    )

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
    bpy.types.Scene.mergeFloat = bpy.props.FloatProperty(
        name = "Int",
        default = 0.02,
        soft_min = 0.00001,
        soft_max = 0.5,
        step = 0.1,

    )
    
    bpy.types.Scene.fixNgons = bpy.props.BoolProperty(
        name = "Tris to quads",
        default = False
    )

def unregister():
    bpy.types.VIEW3D_PT_transform_orientations.remove(extend_transfo_pop_up)
    
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()