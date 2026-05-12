# ##### BEGIN GPL LICENSE BLOCK #####
#
#   Copyright (C) 2020 - 2022  Blake Darrow <contact@blakedarrow.com>
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
import random
import bmesh
import mathutils
from bpy.types import Menu

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

    def draw(self, context):
        layout = self.layout
        objs = context.selected_objects
        all = bpy.data.objects
        layout.label(text="Modeling Tools")
        if len(all) != 0:
            if context.mode == 'EDIT_MESH':
                layout = self.layout
                col = layout.box().column(align=True)
                col.scale_y = 1.33
                col.operator('set.origin', text="Set as Origin", icon="PIVOT_CURSOR")

            if context.mode == 'OBJECT':
                box = layout.box().column(align=True)
                cf = box.column_flow(columns=2, align=True)
                cf.scale_y = 1.2
                cf.operator('move.origin', text="Origin",
                            icon="TRANSFORM_ORIGINS")
                cf.operator('cleanup.mesh', text = "Cleanup", icon="VERTEXSEL")
                cf.operator('shade.smooth', text = "Smooth",icon="MOD_SMOOTH")
                cf.operator("unwrap.selected", text="Unwrap", icon="UV")
                cf.operator('apply.transforms', text="Transforms",icon="OBJECT_ORIGIN")
                cf.operator('apply.normals', text="Normals", icon="ORIENTATION_NORMAL")
                cf.operator('shade.sharp', text="Sharp", icon="MOD_NOISE")
                cf.operator('darrow.move_on_grid', text="Align", icon="MOD_LATTICE")

                if len(objs) == 0:
                    cf.enabled = False
                else:
                    cf.enabled = True
                
                # LOD Generator button
                box.separator()
                lod_row = box.row(align=True)
                lod_row.scale_y = 1.3
                lod_row.operator('darrow.generate_lods', text="LOD Gen", icon="MOD_DECIM")
                if len(objs) == 0:
                    lod_row.enabled = False

class DARROW_PT_toolExtendPanel(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolPanel"
    bl_label = "More Tools"

    def draw(self, context):
        none = None

class DARROW_PT_toolPanel_2(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolExtendPanel"
    bl_label = "Align on Grid"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        all = bpy.data.objects
        if len(all) != 0:
            layout = self.layout
            scn = context.scene
            col = layout.column(align=True)
            col.scale_y = 1.33
            
            col.prop(scn, "alignGridRows", text="Row Amount", slider = True)
            col.prop(scn, "alignGridSpacing", text="Object Padding", slider = True)
            col.prop(scn, "alignGridHeight", text="Offset Height", slider = True)
            col.separator()
            btn = col.row(align = True)
            btn.scale_y = 1.5
            btn.operator("darrow.move_on_grid", text="Align on Grid", icon="MOD_LATTICE")

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
            prnt = layout.column()
            prnt.scale_y = 1.33

            col = prnt.column(align=True)
            amt = col.column(align=True)
            row = col.row(align=True)
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
            
            amt.prop(context.scene, 'arrayAmount', slider=True)
            prnt.separator()

            array = prnt.split(align=True).row(align=True)
            array.scale_y = 1.5
            array.operator('circle.array',text="Array Around Cursor", icon="ONIONSKIN_ON",)
            array.operator('clear.array', text="", icon="TRASH")
        
          
            if len(objs) != 0:
                col.enabled = True

            if xAxis or yAxis or zAxis and len(objs) != 0:
                array.enabled = True
            else:
                array.enabled = False


            if context.mode != 'OBJECT':
                array.enabled = False

class DARROW_PT_toolPanel_4(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolExtendPanel"
    bl_label = "Unwrap"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        all = bpy.data.objects
        if len(all) != 0:
            objs = context.selected_objects
            layout = self.layout
            scn = context.scene

            prnt = layout.column(align=True)
            prnt.scale_y = 1.33
           
            prop = prnt.column(align=True)
            prop.prop(scn, "unwrapAngle", text="Angle Limit", slider=True)

            col = prnt.column(align=True).split(align=True)

            row_seam = col.row(align=True)
            generate_seam = row_seam.split(align=True)
            split_seam = row_seam.split(align=True)

            generate_seam.prop(scn, "seam", text="Seam", toggle=True)
            split_seam.operator("clear.seam", text="", icon="TRASH")

            row_sharp = col.row(align=True)
            generate_sharp = row_sharp.split(align=True)
            split_sharp = row_sharp.split(align=True)

            generate_sharp.prop(scn, "sharp", text="Sharp", toggle=True)
            split_sharp.operator("clear.sharp", text="", icon="TRASH")

            prnt.separator()
            
            # Texel Density Settings
            texel_box = prnt.column(align=True)
            texel_box.prop(scn, "useTexelDensity", text="Use Texel Density", toggle=True)
            
            if scn.useTexelDensity:
                texel_col = texel_box.column(align=True)
                texel_col.prop(scn, "textureResolution", text="Texture Size")
                
                # Unit selector
                texel_col.prop(scn, "texelDensityUnit", text="Unit")
                
                # Show appropriate preset based on unit
                if scn.texelDensityUnit == 'PX_M':
                    texel_col.prop(scn, "texelDensityPresetMeters", text="Density")
                    td_value = float(scn.texelDensityPresetMeters)
                    texel_col.label(text=f"= {td_value:.2f} px/m", icon='INFO')
                else:
                    texel_col.prop(scn, "texelDensityPresetCentimeters", text="Density")
                    td_value = float(scn.texelDensityPresetCentimeters)
                    texel_col.label(text=f"= {td_value:.2f} px/cm", icon='INFO')
            
            prnt.separator()
            unwrap = prnt.row(align=True)
            unwrap.scale_y = 1.5
            unwrap.operator("unwrap.selected", text="Unwrap Objects", icon="UV")
            unwrap.operator("clear.uvs", text="", icon="TRASH")

            if len(objs) == 0 and context.mode != 'EDIT_MESH':
                split_sharp.enabled = False
                split_seam.enabled = False
                unwrap.enabled = False

class DARROW_PT_toolPanel_5(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolExtendPanel"
    bl_label = "Vertex Color"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        all = bpy.data.objects
        if len(all) != 0:
            Var_displayBool = bpy.context.scene.vertexDisplayBool
            Var_viewportShading = bpy.context.space_data.shading.type
            objs = context.selected_objects

            layout = self.layout   
            layout.scale_y = 1.33
            col = layout.column()
            if Var_displayBool == True:
                col.operator('set.display', icon="HIDE_OFF",
                                     text="Hide Colors", depress=Var_displayBool)
            else:
                col.operator('set.display', icon="HIDE_ON",
                                     text="Visualize Colors", depress=Var_displayBool)
            if Var_viewportShading != 'SOLID':
                col.enabled = False
            prnt = layout.column(align=True)
            split = prnt.column(align=True)
            row = split.row(align=True)

            row.operator('set.black')
            row.operator('set.white')

            if len(objs) == 0:
                row.enabled = False

            row = split.row(align=True)

            row.operator('set.red')
            row.operator('set.green')
            row.operator('set.blue')

            prnt.separator()
            color = prnt.row(align=True)
            color.scale_y = 1.5
            color.prop(context.scene, "colorPicker", text="")
            
            if len(objs) == 0:
                row.enabled = False
                color.enabled = False
 
class DARROW_PT_toolPanel_6(DarrowToolPanel, bpy.types.Panel):
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
            prnt = layout.column(align=True)
            prnt.scale_y = 1.33

            col = prnt.column(align=True)
            col.prop(settings, "removeDoublesAmount", text="Merge Distance",slider=True)
            col.prop(scn, "fixNgons", text="Triangulate then Quad", toggle=True)

            prnt.separator()
            clean = prnt.column(align=True)
            clean.scale_y = 1.5
            clean.operator("cleanup.mesh", text="Cleanup Selected", icon= "VERTEXSEL")
            if len(objs) == 0:
                col.enabled = False

class DARROW_PT_toolPanel_7(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolExtendPanel"
    bl_label = "Orientations"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        cf2 = layout.column_flow(columns=2, align=True)
        cf2.scale_y = 1.33

        cf2.operator('view.create_orient', text="Set", icon="RESTRICT_SELECT_OFF")
        cf2.operator('clear.orientation', text="Clear", icon="TRASH")

class DARROW_PT_toolPanel_8(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolExtendPanel"
    bl_label = "Custom Properties"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        objs = context.selected_objects
        layout = self.layout
        col = layout.column(align=True)
        col.scale_y = 1.33
        btn = col.row(align=True)
        btn.operator('darrow.set_is_cutter', text="Set is_cutter", icon="SCULPTMODE_HLT")
        btn2 = col.row(align=True)
        btn2.operator('darrow.set_static_bevel', text="Set static_bevel", icon="MOD_BEVEL")
        if len(objs) == 0:
            btn.enabled = False
            btn2.enabled = False

class DarrowSetIsCutter(bpy.types.Operator):
    bl_idname = "darrow.set_is_cutter"
    bl_label = "Set is_cutter"
    bl_description = "Add 'is_cutter' custom property (True) to selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) == 0:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        for obj in objs:
            obj["is_cutter"] = True
        self.report({'INFO'}, f"Set 'is_cutter' on {len(objs)} object(s)")
        return {'FINISHED'}

class DarrowSetStaticBevel(bpy.types.Operator):
    bl_idname = "darrow.set_static_bevel"
    bl_label = "Set static_bevel"
    bl_description = "Mark selected objects to preserve bevel segments during LOD generation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) == 0:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        for obj in objs:
            obj["set_static_bevel"] = True
        self.report({'INFO'}, f"Set 'set_static_bevel' on {len(objs)} object(s)")
        return {'FINISHED'}

#-----------------------------------------------------#  
#   LOD Generator
#-----------------------------------------------------#

class DARROW_PT_toolPanel_LOD(DarrowToolPanel, bpy.types.Panel):
    bl_parent_id = "DARROW_PT_toolExtendPanel"
    bl_label = "LOD Generator"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        all = bpy.data.objects
        if len(all) != 0:
            objs = context.selected_objects
            layout = self.layout
            scn = context.scene

            prnt = layout.column(align=True)
            prnt.scale_y = 1.33

            # LOD Count
            col = prnt.column(align=True)
            col.prop(scn, "lodCount", text="LOD Levels", slider=True)
            
            # Final LOD Type
            col.prop(scn, "lodFinalType", text="Final LOD")
            
            prnt.separator()
            
            # Dynamic LOD Ratios based on count
            lod_count = scn.lodCount
            if lod_count > 2:  # Only show ratios if there are intermediate LODs
                ratio_box = prnt.column(align=True)
                ratio_box.label(text="Decimation Ratios:")
                ratio_col = ratio_box.column(align=True)
                
                # Show ratio sliders for intermediate LODs (not LOD0 or final)
                ratio_props = ["lodRatio1", "lodRatio2", "lodRatio3", "lodRatio4", "lodRatio5"]
                for i in range(1, lod_count - 1):
                    if i <= len(ratio_props):
                        ratio_col.prop(scn, ratio_props[i-1], text=f"LOD{i}")
                
                prnt.separator()
            
            # Options
            opt_box = prnt.column(align=True)
            opt_box.label(text="Options:")
            opt_col = opt_box.column(align=True)
            
            row = opt_col.row(align=True)
            row.prop(scn, "lodPreserveUVs", text="Preserve UVs", toggle=True)
            row.prop(scn, "lodKeepMaterials", text="Materials", toggle=True)
            
            row = opt_col.row(align=True)
            row.prop(scn, "lodTriangulate", text="Triangulate", toggle=True)
            row.prop(scn, "lodApplyModifiers", text="Apply Mods", toggle=True)
            
            row = opt_col.row(align=True)
            row.prop(scn, "lodShadeSmooth", text="Shade Smooth", toggle=True)
            row.prop(scn, "lodSmartUnbevel", text="Un-Bevel", toggle=True)
            
            prnt.separator()
            
            # Generate button
            gen = prnt.row(align=True)
            gen.scale_y = 1.5
            gen.operator("darrow.generate_lods", text="Generate LODs", icon="MOD_DECIM")
            
            # Enable/disable based on selection
            valid_selection = False
            for obj in objs:
                if obj.type == 'MESH' or obj.type == 'EMPTY':
                    valid_selection = True
                    break
                # Check if it's a collection instance or we have an active collection
            
            if len(objs) == 0:
                gen.enabled = False
            elif not valid_selection:
                gen.enabled = False


class DarrowGenerateLODs(bpy.types.Operator):
    bl_idname = "darrow.generate_lods"
    bl_label = "Generate LODs"
    bl_description = "Generate LOD chain from selected Empty, Collection, or meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def is_boolean_cutter(self, obj):
        """Check if object is used as a boolean cutter anywhere in the scene"""
        # Check for is_cutter custom property
        if obj.get("is_cutter", False):
            return True
        
        # Check if this object is used as a boolean operand by any other object
        for scene_obj in bpy.data.objects:
            if scene_obj.type == 'MESH':
                for mod in scene_obj.modifiers:
                    if mod.type == 'BOOLEAN' and mod.object == obj:
                        return True
        return False

    def should_skip_object(self, obj):
        """Check if object should be skipped for LOD generation"""
        # Skip if render is disabled
        if obj.hide_render:
            return True
        # Skip if it's a boolean cutter
        if self.is_boolean_cutter(obj):
            return True
        return False

    def is_convertible_to_mesh(self, obj):
        """Check if object type can be converted to mesh"""
        return obj.type in {'CURVE', 'SURFACE', 'FONT', 'META'}

    def get_meshes_recursive(self, obj):
        """Recursively get all mesh children of an object, skipping render-disabled and cutters"""
        meshes = []
        if (obj.type == 'MESH' or self.is_convertible_to_mesh(obj)) and not self.should_skip_object(obj):
            meshes.append(obj)
        for child in obj.children:
            meshes.extend(self.get_meshes_recursive(child))
        return meshes

    def get_collection_meshes_recursive(self, collection):
        """Recursively get all meshes from a collection and its children"""
        meshes = []
        for obj in collection.objects:
            if (obj.type == 'MESH' or self.is_convertible_to_mesh(obj)) and not self.should_skip_object(obj):
                meshes.append(obj)
        for child_col in collection.children:
            meshes.extend(self.get_collection_meshes_recursive(child_col))
        return meshes

    def create_bounding_box(self, source_obj, name):
        """Create a bounding box mesh from source object"""
        # Get bounding box corners in world space
        bbox_corners = [source_obj.matrix_world @ mathutils.Vector(corner) for corner in source_obj.bound_box]
        
        # Create mesh from bounding box
        mesh = bpy.data.meshes.new(name)
        
        # Define vertices (8 corners of bounding box)
        verts = [corner[:] for corner in bbox_corners]
        
        # Define faces (6 faces of the box)
        faces = [
            (0, 1, 2, 3),  # bottom
            (4, 7, 6, 5),  # top
            (0, 4, 5, 1),  # front
            (2, 6, 7, 3),  # back
            (0, 3, 7, 4),  # left
            (1, 5, 6, 2),  # right
        ]
        
        mesh.from_pydata(verts, [], faces)
        mesh.validate()
        mesh.update()
        
        # Create object
        bbox_obj = bpy.data.objects.new(name, mesh)
        bbox_obj.location = (0, 0, 0)
        
        return bbox_obj

    def create_convex_hull(self, source_obj, name):
        """Create a convex hull mesh from source object using bmesh"""
        # Get all vertex positions in world space from source mesh
        source_mesh = source_obj.data
        matrix = source_obj.matrix_world
        
        world_verts = [matrix @ mathutils.Vector(v.co) for v in source_mesh.vertices]
        
        if len(world_verts) < 4:
            # Not enough verts for convex hull, return copy
            mesh = source_obj.data.copy()
            hull_obj = bpy.data.objects.new(name, mesh)
            return hull_obj
        
        # Create bmesh and add vertices
        bm = bmesh.new()
        for co in world_verts:
            bm.verts.new(co)
        bm.verts.ensure_lookup_table()
        
        # Create convex hull using bmesh operator
        try:
            result = bmesh.ops.convex_hull(bm, input=bm.verts)
            # Remove interior geometry
            bmesh.ops.delete(bm, geom=result['geom_interior'], context='VERTS')
        except Exception as e:
            # Fallback: just use vertices as-is
            bm.free()
            mesh = source_obj.data.copy()
            hull_obj = bpy.data.objects.new(name, mesh)
            return hull_obj
        
        # Create new mesh from bmesh
        hull_mesh = bpy.data.meshes.new(name)
        bm.to_mesh(hull_mesh)
        bm.free()
        
        # Ensure mesh is valid
        hull_mesh.validate()
        hull_mesh.update()
        
        # Create object (not linked to any collection yet)
        hull_obj = bpy.data.objects.new(name, hull_mesh)
        hull_obj.location = (0, 0, 0)  # Vertices are already in world space
        
        return hull_obj

    def backup_and_reduce_bevels(self, source_objects):
        """Backup bevel segments and reduce to 1 on source objects and their boolean cutters.
        Returns dict for restoration."""
        bevel_backup = {}  # {obj: {mod_name: segments}}
        
        for obj in source_objects:
            # Skip if object has set_static_bevel
            if obj.get("set_static_bevel", False):
                continue
            
            if obj.type != 'MESH':
                continue
                
            for mod in obj.modifiers:
                # Reduce bevel segments on the object itself
                if mod.type == 'BEVEL':
                    if obj not in bevel_backup:
                        bevel_backup[obj] = {}
                    if mod.name not in bevel_backup[obj]:
                        bevel_backup[obj][mod.name] = mod.segments
                    mod.segments = 1
                
                # Also handle boolean cutters
                if mod.type == 'BOOLEAN' and mod.object:
                    cutter = mod.object
                    # Skip cutter if it has set_static_bevel
                    if cutter.get("set_static_bevel", False):
                        continue
                    
                    for cutter_mod in cutter.modifiers:
                        if cutter_mod.type == 'BEVEL':
                            if cutter not in bevel_backup:
                                bevel_backup[cutter] = {}
                            if cutter_mod.name not in bevel_backup[cutter]:
                                bevel_backup[cutter][cutter_mod.name] = cutter_mod.segments
                            cutter_mod.segments = 1
        
        return bevel_backup

    def restore_bevels(self, bevel_backup):
        """Restore bevel segments from backup."""
        for obj, mods in bevel_backup.items():
            for mod_name, segments in mods.items():
                if mod_name in obj.modifiers:
                    obj.modifiers[mod_name].segments = segments

    def extract_evaluated_geometry(self, context, source_objects):
        """Extract all evaluated geometry from source objects using depsgraph.
        Returns combined bmesh and list of collected materials."""
        
        # Build set of source object names for matching
        source_names = {obj.name for obj in source_objects}
        
        # Get fresh depsgraph
        depsgraph = context.evaluated_depsgraph_get()
        
        # Combined bmesh for all geometry
        combined_bm = bmesh.new()
        collected_materials = []
        material_index_map = {}  # material -> index in collected_materials
        
        instance_count = 0
        
        for instance in depsgraph.object_instances:
            # Get the original object this instance belongs to
            parent_obj = instance.parent if instance.parent else instance.object
            
            # Check if this instance belongs to one of our selected objects
            belongs_to_selection = False
            if instance.object.original.name in source_names:
                belongs_to_selection = True
            elif parent_obj and parent_obj.original.name in source_names:
                belongs_to_selection = True
            
            if not belongs_to_selection:
                continue
            
            # Skip non-mesh instances
            obj = instance.object
            if obj.type != 'MESH':
                continue
            
            # Get evaluated mesh data using new_from_object (safer than to_mesh)
            try:
                mesh_eval = bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph))
            except:
                continue
            
            if mesh_eval is None or len(mesh_eval.vertices) == 0:
                bpy.data.meshes.remove(mesh_eval)
                continue
            
            instance_count += 1
            
            # Get the instance's world matrix
            matrix = instance.matrix_world.copy()
            
            # Collect materials from this mesh
            for mat_slot in mesh_eval.materials:
                if mat_slot and mat_slot not in material_index_map:
                    material_index_map[mat_slot] = len(collected_materials)
                    collected_materials.append(mat_slot)
            
            # Create temp bmesh, transform, and merge into combined
            temp_bm = bmesh.new()
            temp_bm.from_mesh(mesh_eval)
            temp_bm.transform(matrix)
            
            # Remap material indices
            for face in temp_bm.faces:
                if face.material_index < len(mesh_eval.materials):
                    mat = mesh_eval.materials[face.material_index]
                    if mat and mat in material_index_map:
                        face.material_index = material_index_map[mat]
                    else:
                        face.material_index = 0
            
            # Convert to temp mesh and merge into combined bmesh
            if temp_bm.faces:
                merge_mesh = bpy.data.meshes.new("_merge_temp")
                temp_bm.to_mesh(merge_mesh)
                combined_bm.from_mesh(merge_mesh)
                bpy.data.meshes.remove(merge_mesh)
            
            temp_bm.free()
            bpy.data.meshes.remove(mesh_eval)
        
        return combined_bm, collected_materials, instance_count

    def execute(self, context):
        scn = context.scene
        selected = context.selected_objects[:]  # Copy list
        
        if len(selected) == 0:
            self.report({'ERROR'}, "Nothing selected")
            return {'CANCELLED'}
        
        # Determine source meshes and base name
        source_meshes = []
        base_name = ""
        
        # Check if we have an Empty selected
        empty_selected = None
        for obj in selected:
            if obj.type == 'EMPTY':
                empty_selected = obj
                break
        
        if empty_selected:
            # Get all mesh children recursively
            source_meshes = self.get_meshes_recursive(empty_selected)
            base_name = empty_selected.name
            if len(source_meshes) == 0:
                self.report({'ERROR'}, "Empty has no valid mesh children (check render visibility and boolean cutters)")
                return {'CANCELLED'}
        else:
            # Check for mesh selection (including convertible types like curves)
            mesh_count = 0
            for obj in selected:
                if (obj.type == 'MESH' or self.is_convertible_to_mesh(obj)) and not self.should_skip_object(obj):
                    source_meshes.append(obj)
                    mesh_count += 1
            
            if mesh_count == 0:
                self.report({'ERROR'}, "No valid meshes found (check render visibility and boolean cutters)")
                return {'CANCELLED'}
            
            if mesh_count > 1:
                # Multiple meshes require a common parent Empty
                parents = set()
                for obj in source_meshes:
                    if obj.parent and obj.parent.type == 'EMPTY':
                        parents.add(obj.parent)
                
                if len(parents) == 1:
                    base_name = list(parents)[0].name
                else:
                    self.report({'ERROR'}, "Multiple meshes selected - please select their parent Empty instead")
                    return {'CANCELLED'}
            else:
                base_name = source_meshes[0].name
        
        # Create LOD collection
        lod_collection_name = f"{base_name}_LODs"
        if lod_collection_name in bpy.data.collections:
            # Remove existing LOD collection
            old_col = bpy.data.collections[lod_collection_name]
            for obj in list(old_col.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(old_col)
        
        lod_collection = bpy.data.collections.new(lod_collection_name)
        bpy.context.scene.collection.children.link(lod_collection)
        lod_collection.color_tag = 'COLOR_04'
        
        # Deselect all objects without using operators
        for obj in context.selected_objects:
            obj.select_set(False)
        
        # === DEPSGRAPH-BASED LOD0 GENERATION ===
        
        # Smart Un-Bevel: temporarily reduce bevel segments on ORIGINAL objects
        # DISABLED - modifying source objects can corrupt depsgraph
        bevel_backup = {}
        # if scn.lodSmartUnbevel:
        #     bevel_backup = self.backup_and_reduce_bevels(source_meshes)
        
        # Extract evaluated geometry from depsgraph (captures geo nodes, booleans, etc.)
        combined_bm, collected_materials, instance_count = self.extract_evaluated_geometry(context, source_meshes)
        
        # Restore original bevel segments
        # if bevel_backup:
        #     self.restore_bevels(bevel_backup)
        
        if instance_count == 0 or not combined_bm.faces:
            combined_bm.free()
            self.report({'ERROR'}, "No geometry could be extracted from selection")
            return {'CANCELLED'}
        
        # Create LOD0 mesh from combined bmesh
        lod0_mesh = bpy.data.meshes.new(f"{base_name}_LOD0")
        combined_bm.to_mesh(lod0_mesh)
        combined_bm.free()
        
        # Add materials to mesh
        for mat in collected_materials:
            lod0_mesh.materials.append(mat)
        
        # Create LOD0 object
        lod0 = bpy.data.objects.new(f"{base_name}_LOD0", lod0_mesh)
        lod_collection.objects.link(lod0)
        
        # Triangulate if requested (using bmesh)
        if scn.lodTriangulate:
            bm = bmesh.new()
            bm.from_mesh(lod0.data)
            bmesh.ops.triangulate(bm, faces=bm.faces[:])
            bm.to_mesh(lod0.data)
            bm.free()
            lod0.data.update()
        
        # Generate intermediate LODs
        lod_count = scn.lodCount
        lods_created = [lod0]
        
        # Get ratios from scene properties
        lod_ratios = [1.0, scn.lodRatio1, scn.lodRatio2, scn.lodRatio3, scn.lodRatio4, scn.lodRatio5]
        
        for i in range(1, lod_count - 1):
            ratio = lod_ratios[i] if i < len(lod_ratios) else 0.05
            ratio = max(0.01, ratio)
            
            # Create decimated LOD mesh directly
            lod_mesh = lod0.data.copy()
            lod_mesh.name = f"{base_name}_LOD{i}_temp"
            
            # Create temp object for decimation
            temp_obj = bpy.data.objects.new("_temp_decimate", lod_mesh)
            context.scene.collection.objects.link(temp_obj)
            
            # Add decimate modifier
            decimate = temp_obj.modifiers.new(name="LOD_Decimate", type='DECIMATE')
            decimate.decimate_type = 'COLLAPSE'
            decimate.ratio = ratio
            if scn.lodPreserveUVs:
                decimate.use_collapse_triangulate = False
            
            # Get evaluated mesh through depsgraph
            depsgraph = context.evaluated_depsgraph_get()
            
            # Create final mesh from evaluated object
            final_mesh = bpy.data.meshes.new_from_object(temp_obj.evaluated_get(depsgraph))
            final_mesh.name = f"{base_name}_LOD{i}"
            
            # Create the actual LOD object with the final mesh
            lod_n = bpy.data.objects.new(f"{base_name}_LOD{i}", final_mesh)
            lod_collection.objects.link(lod_n)
            
            # Remove temp object from scene
            context.scene.collection.objects.unlink(temp_obj)
            bpy.data.objects.remove(temp_obj)
            bpy.data.meshes.remove(lod_mesh)
            
            lods_created.append(lod_n)
        
        # Generate final LOD (bounding box or convex hull)
        final_lod_name = f"{base_name}_LOD{lod_count - 1}"
        
        if scn.lodFinalType == 'BBOX':
            final_lod = self.create_bounding_box(lod0, final_lod_name)
        else:
            final_lod = self.create_convex_hull(lod0, final_lod_name)
        
        lod_collection.objects.link(final_lod)
        
        # Copy materials if requested
        if scn.lodKeepMaterials and lod0.data.materials:
            for mat in lod0.data.materials:
                if mat:
                    final_lod.data.materials.append(mat)
        
        lods_created.append(final_lod)
        
        # Copy materials to intermediate LODs
        if scn.lodKeepMaterials:
            for lod in lods_created[1:-1]:
                lod.data.materials.clear()
                for mat in lod0.data.materials:
                    lod.data.materials.append(mat)
        
        # Apply smooth shading using shade_auto_smooth operator
        # Check property with explicit True default (handles uninitialized state)
        try:
            shade_smooth_enabled = scn.lodShadeSmooth
        except:
            shade_smooth_enabled = True
        
        print(f"DEBUG: lodShadeSmooth = {shade_smooth_enabled}, lods_created count = {len(lods_created)}")
        
        if shade_smooth_enabled:
            for lod in lods_created:
                if lod and lod.type == 'MESH' and lod.data:
                    print(f"DEBUG: Applying shade_auto_smooth to {lod.name}")
                    # Select only this LOD
                    bpy.ops.object.select_all(action='DESELECT')
                    lod.select_set(True)
                    context.view_layer.objects.active = lod
                    
                    # Merge by distance (remove doubles) using bmesh
                    bm = bmesh.new()
                    bm.from_mesh(lod.data)
                    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
                    bm.to_mesh(lod.data)
                    bm.free()
                    lod.data.update()
                    
                    # Apply auto smooth shading
                    bpy.ops.object.shade_auto_smooth()
                    
                    # Add Weighted Normal modifier
                    wn = lod.modifiers.new(name="Weighted Normal", type='WEIGHTED_NORMAL')
                    wn.mode = 'CORNER_ANGLE'
                    wn.keep_sharp = True
                    print(f"DEBUG: Added Weighted Normal to {lod.name}")
        
        # Select created LODs (direct API, no operators)
        for lod in lods_created:
            lod.select_set(True)
        context.view_layer.objects.active = lods_created[0]
        
        self.report({'INFO'}, f"Generated {lod_count} LODs in '{lod_collection_name}'")
        return {'FINISHED'}

class DarrowMoveOnGrid(bpy.types.Operator):
    bl_label = "Align on Grid"
    bl_idname = "darrow.move_on_grid"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Align selected objects on a grid"

    def execute(self,context):
        zHeight=bpy.context.scene.alignGridHeight
        spacing= bpy.context.scene.alignGridSpacing
    
        objs_sel = bpy.context.selected_objects

        gridSizeY = bpy.context.scene.alignGridRows
        gridSizeX = int(math.ceil(len(objs_sel) / gridSizeY))

        xPosArray = []
        yPosArray = []
        
        for xi in range(0, gridSizeX):
            for yi in range(0, gridSizeY):
                xPos=-(gridSizeX-1)*spacing/2.0+xi*spacing
                yPos=-(gridSizeY-1)*spacing/2.0+yi*spacing

                xPosArray.append(xPos)
                yPosArray.append(yPos)

        i = -1
        random.shuffle(objs_sel)
        for obj in objs_sel:
            i = i +1
            obj.location = (xPosArray[i], yPosArray[i], zHeight)

        return {'FINISHED'}

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

class DarrowSetBlack(bpy.types.Operator):
    bl_idname = "set.black"
    bl_label = "Black"

    def execute(self, context):
        bpy.data.brushes["Draw"].color = (0, 0, 0)
        DarrowSetColor.execute(self, context)
        return {'FINISHED'}

class DarrowSetWhite(bpy.types.Operator):
    bl_idname = "set.white"
    bl_label = "White"

    def execute(self, context):
        bpy.data.brushes["Draw"].color = (1, 1, 1)
        DarrowSetColor.execute(self, context)
        return {'FINISHED'}

def UpdateVertColor(self, context):
    bpy.data.brushes["Draw"].color = context.scene.colorPicker
    DarrowSetColor.execute(self, context)
    return

class DarrowSetRed(bpy.types.Operator):
    bl_idname = "set.red"
    bl_label = "Red"

    def execute(self, context):
        bpy.data.brushes["Draw"].color = (1, 0, 0)
        DarrowSetColor.execute(self, context)
        return {'FINISHED'}

class DarrowSetGreen(bpy.types.Operator):
    bl_idname = "set.green"
    bl_label = "Green"

    def execute(self, context):
        bpy.data.brushes["Draw"].color = (0, 1, 0)
        DarrowSetColor.execute(self, context)
        return {'FINISHED'}

class DarrowSetBlue(bpy.types.Operator):
    bl_idname = "set.blue"
    bl_label = "Blue"

    def execute(self, context):
        bpy.data.brushes["Draw"].color = (0, 0, 1)
        DarrowSetColor.execute(self, context)
        return {'FINISHED'}

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
                if obj.type == 'MESH':
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
                if obj.type == 'MESH':
                    view_layer.objects.active = obj
                    bpy.ops.paint.vertex_paint_toggle()
                    bpy.context.object.data.use_paint_mask = True
                    bpy.ops.paint.vertex_color_set()
                    bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

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

class DarrowCircleArray(bpy.types.Operator):
    bl_idname = "circle.array"
    bl_description = "Move selected to world origin"
    bl_label = "Array Selected"
    bl_options = {"UNDO"}

    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()

        collectionFound = False
        parentCollectionFound = False
        obj = bpy.context.selected_objects[0]
        amt = context.scene.arrayAmount
        settings = context.preferences.addons[__package__].preferences
        selected = bpy.context.selected_objects[0]
        empty_collection_name = "_Empties"
        parent_collection_name = "_SceneOrganizer"

        for myCol in bpy.data.collections:
            
            if myCol.name == parent_collection_name:
                parentCollectionFound = True

            if myCol.name == empty_collection_name:
                collectionFound = True

        if not parentCollectionFound and not collectionFound:
            parentCol = bpy.data.collections.new(parent_collection_name)
            bpy.context.scene.collection.children.link(parentCol)
            bpy.data.collections[parent_collection_name].color_tag = 'COLOR_05'

            col = bpy.data.collections.new(empty_collection_name)
            parentCol.children.link(col)
            bpy.data.collections[empty_collection_name].color_tag = 'COLOR_03'
        
        elif parentCollectionFound and not collectionFound:
            parentCol = bpy.data.collections[parent_collection_name]
            col = bpy.data.collections.new(empty_collection_name)

            parentCol.children.link(col)
            bpy.data.collections[empty_collection_name].color_tag = 'COLOR_03'

        elif not parentCollectionFound and collectionFound:
            col = bpy.data.collections[empty_collection_name]

            bpy.context.scene.collection.children.unlink(col)
            parentCol = bpy.data.collections.new(parent_collection_name)

            bpy.context.scene.collection.children.link(parentCol)
            bpy.data.collections[parent_collection_name].color_tag = 'COLOR_05'

            parentCol.children.link(col)

        elif parentCollectionFound and collectionFound:
            col = bpy.data.collections[empty_collection_name]
        else:
            parentCol = bpy.data.collections.new(parent_collection_name)
            bpy.context.scene.collection.children.link(parentCol)

            col = bpy.data.collections.new(empty_collection_name)
            parentCol.children.link(col)

        bpy.context.scene.cursor.rotation_euler = (0, 0, 0)
        bpy.ops.object.transform_apply(
            location=True, rotation=True, scale=True)
        try:
            if bpy.context.object.modifiers["DarrowToolsArray"].offset_object == None:
                modifier_to_remove = obj.modifiers.get("DarrowToolsArray")
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
            empty = bpy.data.objects[context.object.linkedEmpty]

        bpy.ops.object.select_all(action='DESELECT')
        selected.select_set(state=True)
        context.view_layer.objects.active = selected
        context.object.linkedEmpty = empty.name
        array = False
        mod = bpy.context.object

        for modifier in mod.modifiers:
            if modifier.name == "DarrowToolsArray":
                array = True

        if not array:
            modifier = obj.modifiers.new(
                name='DarrowToolsArray', type='ARRAY')

            modifier.name = "DarrowToolsArray"
            modifier.count = amt
            modifier.use_relative_offset = False
            modifier.use_object_offset = True
            modifier.offset_object = empty
        else:
            modifier_to_remove = obj.modifiers.get("DarrowToolsArray")
            obj.modifiers.remove(modifier_to_remove)

            modifier = obj.modifiers.new(
                name='DarrowToolsArray', type='ARRAY')

            modifier.name = "DarrowToolsArray"
            modifier.count = amt
            modifier.use_relative_offset = False
            modifier.use_object_offset = True
            modifier.offset_object = empty

        modAmt = -1
        for mod in (obj.modifiers):
           modAmt = modAmt + 1

        bpy.ops.object.modifier_move_to_index(
            modifier="DarrowToolsArray", index=modAmt)
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
            if modifier.name == "DarrowToolsArray":
                modifier_to_remove = obj.modifiers.get("DarrowToolsArray")
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

class DarrowTransforms(bpy.types.Operator):
    bl_idname = "apply.transforms"
    bl_description = "Apply rotation and scale to selected object"
    bl_label = "Apply Rot & Scale"
    bl_options = {"UNDO"}

    def execute(self, context):

        objs = context.selected_objects
        if len(objs) != 0: 
            active = bpy.context.view_layer.objects.active
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None

            for obj in objs:
                obj.select_set(state=True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=True)
                bpy.ops.object.transform_apply(location=False,rotation=True, scale=True)
                obj.select_set(state=False)
            
            for obj in objs:
                obj.select_set(True)

            bpy.context.view_layer.objects.active = active

            self.report({'INFO'}, "Transforms applied")
        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}

class DarrowSetOrigin(bpy.types.Operator):
    bl_idname = "set.origin"
    bl_description = "Set selected as object origin"
    bl_label = "Set Origin"

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) != 0: 
            if context.mode == 'OBJECT':
                bpy.ops.object.editmode_toggle()

            x, y, z = bpy.context.scene.cursor.location.x,  bpy.context.scene.cursor.location.y, bpy.context.scene.cursor.location.z
            print(bpy.context.scene.cursor.location.x)

            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

            bpy.context.scene.cursor.location = (x,y,z)

            self.report({'INFO'}, "Selected is now origin")
        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}

class DarrowMoveOrigin(bpy.types.Operator):
    bl_idname = "move.origin"
    bl_description = "Move selected to world origin"
    bl_label = "Move to Origin"

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) != 0: 

            x, y, z = bpy.context.scene.cursor.location.x,  bpy.context.scene.cursor.location.y, bpy.context.scene.cursor.location.z
            bpy.ops.view3d.snap_cursor_to_center()
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
            bpy.context.scene.cursor.location = (x,y,z)
            self.report({'INFO'}, "Moved selected to object origin")
        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}
  
class DarrowNormals(bpy.types.Operator):
    bl_idname = "apply.normals"
    bl_description = "Calculate outside normals"
    bl_label = "Calculate Normals"

    def execute(self, context):
        objs = bpy.context.selected_objects
        active = bpy.context.view_layer.objects.active

        if len(objs) != 0: 
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None

            for obj in objs:
                if obj.type == "MESH":
                    obj.select_set(state=True)
                    bpy.context.view_layer.objects.active = obj

                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.normals_make_consistent(inside=False)
                    bpy.ops.object.editmode_toggle()
                    obj.select_set(state=False)

            for obj in objs:
                if obj.type == "MESH":
                    obj.select_set(True)

            bpy.context.view_layer.objects.active = active

            self.report({'INFO'}, "Normals calculated outside")

        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}
      
class DarrowSmooth(bpy.types.Operator):
    bl_idname = "shade.smooth"
    bl_label = "Smooth Object"
    bl_description = "Smooth the selected object"

    def execute(self, context):
        objs = context.selected_objects
        if len(objs) != 0: 
            active = bpy.context.view_layer.objects.active
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None

            for obj in objs:
                if obj.type == "MESH":
                    obj.select_set(state=True)
                    bpy.context.view_layer.objects.active = obj
                    # Use shade_smooth_by_angle for Blender 4.1+
                    try:
                        bpy.ops.object.shade_smooth_by_angle(angle=3.14159)
                    except:
                        bpy.ops.object.shade_smooth()
                    obj.select_set(state=False)
            
            for obj in objs:
                if obj.type == "MESH":
                    obj.select_set(True)

            bpy.context.view_layer.objects.active = active
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
            bpy.ops.object.select_all(action='DESELECT')
            active = bpy.context.view_layer.objects.active
            bpy.context.view_layer.objects.active = None

            for obj in objs:
                if obj.type == "MESH":
                    obj.select_set(state=True)
                    bpy.context.view_layer.objects.active = obj
                    # Use shade_smooth_by_angle with 0 for sharp look
                    try:
                        bpy.ops.object.shade_smooth_by_angle(angle=0)
                    except:
                        bpy.ops.object.shade_flat()
                    obj.select_set(state=False)

            for obj in objs:
                if obj.type == "MESH":
                    obj.select_set(True)

            bpy.context.view_layer.objects.active = active

            self.report({'INFO'}, "Object smoothed to 0")
        else:
            self.report({'INFO'}, "None Selected")
        return {'FINISHED'}

class DarrowClearSharp(bpy.types.Operator):
    bl_idname = "clear.sharp"
    bl_label = "Clear sharp edges"
    bl_description = "Clear all sharp edges"

    def execute(self, context):
        selection = bpy.context.selected_objects
        object_mode = False

        if context.mode == 'OBJECT':
            object_mode = True
            bpy.ops.object.select_all(action='DESELECT')
        else:
            bpy.ops.mesh.select_all(action='DESELECT')
            object_mode = False
        
        for i in selection:
            if i.type == "MESH":
                i.select_set(True)
                bpy.context.view_layer.objects.active = i
                obj = bpy.context.active_object

                bpy.ops.object.mode_set(mode="OBJECT")

                if obj is not None and obj.type == 'MESH':
                    bm = bmesh.new()
                    bm.from_mesh(obj.data)

                    for edge in bm.edges:
                        edge.smooth = True

                    bm.to_mesh(obj.data)
                    bm.free()
                
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode="OBJECT")
                i.select_set(False)

        if object_mode:   
            bpy.ops.object.mode_set(mode="OBJECT")
        else:
            for i in selection:
                i.select_set(True)
            bpy.ops.object.mode_set(mode="EDIT")
            
        for i in selection:
            i.select_set(True)
      
        self.report({'INFO'}, "Cleared all Seams")
        return {'FINISHED'}
    
class DarrowClearSeam(bpy.types.Operator):
    bl_idname = "clear.seam"
    bl_label = "Clear seamed edges"
    bl_description = "Clear all seam edges"

    def execute(self, context):
        selection = bpy.context.selected_objects
        object_mode = False
        if context.mode == 'OBJECT':
            object_mode = True
            bpy.ops.object.select_all(action='DESELECT')
        else:
            bpy.ops.mesh.select_all(action='DESELECT')
        
        for i in selection:
            if i.type == "MESH":
                i.select_set(True)
                bpy.context.view_layer.objects.active = i
                obj = bpy.context.active_object
                if context.mode != 'OBJECT':
                    bpy.ops.object.editmode_toggle()

                if obj is not None and obj.type == 'MESH':
                    bm = bmesh.new()
                    bm.from_mesh(obj.data)

                    for edge in bm.edges:
                        edge.seam = False

                    bm.to_mesh(obj.data)
                    bm.free()
                
                if context.mode == 'OBJECT':
                    bpy.ops.object.editmode_toggle()
                
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode="OBJECT")

                i.select_set(False)

        if object_mode:   
            bpy.ops.object.mode_set(mode="OBJECT")
        else:
            for i in selection:
                i.select_set(True)
            bpy.ops.object.mode_set(mode="EDIT")
            
        for i in selection:
            i.select_set(True)
                
        self.report({'INFO'}, "Cleared all Seams")
        return {'FINISHED'}

class DarrowClearUVs(bpy.types.Operator):
    bl_idname = "clear.uvs"
    bl_label = "Clear UVs"
    bl_description = "Clear all UVs"

    def execute(self, context):
        selection = bpy.context.selected_objects

        for i in selection:
            if i.type == "MESH":
                bpy.context.view_layer.objects.active = i
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.uv.reset()
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}

def updateSharpSeam(self, context):
    unwrap_angle = math.radians(bpy.context.scene.unwrapAngle)
    selection = bpy.context.selected_objects
    
    if not (bpy.context.scene.sharp or bpy.context.scene.seam):
        return

    # Store original mode
    original_mode = context.mode
    
    for i in selection:
        if i.type == "MESH":
            # Make sure we're in object mode
            if context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            
            bpy.context.view_layer.objects.active = i
            obj = bpy.context.active_object
            
            if obj is not None and obj.type == 'MESH':
                bm = bmesh.new()
                bm.from_mesh(obj.data)

                for edge in bm.edges:
                    # Reset edges first
                    edge.seam = False
                    edge.smooth = True
                    
                    # Only calculate angle for edges that have exactly 2 faces
                    if len(edge.link_faces) == 2:
                        angle = edge.calc_face_angle()
                        
                        if angle > unwrap_angle:
                            if bpy.context.scene.sharp:
                                edge.smooth = False  # Mark edge as sharp
                            if bpy.context.scene.seam:
                                edge.seam = True  # Mark edge as seam
                    else:
                        # For boundary edges or non-manifold geometry
                        if bpy.context.scene.sharp:
                            edge.smooth = False
                        if bpy.context.scene.seam:
                            edge.seam = True
                        
                bm.to_mesh(obj.data)
                bm.free()
    
    # Restore original mode
    if original_mode == 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='EDIT')
    
    # Reselect objects
    for i in selection:
        i.select_set(True)
                
class DarrowUnwrapSelected(bpy.types.Operator):
    bl_label = "Example"
    bl_idname = "unwrap.selected"
    bl_description = "Unwrap all selection with optional texel density"
    bl_options = {'REGISTER', 'UNDO'}

    def mark_edges_for_unwrap(self, obj):
        """Mark sharp/seam edges based on angle"""
        unwrap_angle = math.radians(bpy.context.scene.unwrapAngle)
        
        if obj is not None and obj.type == 'MESH':
            bm = bmesh.new()
            bm.from_mesh(obj.data)

            for edge in bm.edges:
                # Only calculate angle for edges that have exactly 2 faces
                if len(edge.link_faces) == 2:
                    angle = edge.calc_face_angle()

                    if angle > unwrap_angle:
                        if bpy.context.scene.sharp:
                            edge.smooth = False  # Mark edge as sharp
                        if bpy.context.scene.seam:
                            edge.seam = True  # Mark edge as seam
                else:
                    # For boundary edges or non-manifold geometry, mark as seam/sharp
                    if bpy.context.scene.sharp:
                        edge.smooth = False
                    if bpy.context.scene.seam:
                        edge.seam = True
            
            bm.to_mesh(obj.data)
            bm.free()

    def batch_unwrap(self, objects, use_seam_sharp):
        """Unwrap multiple objects together"""
        scn = bpy.context.scene
        unwrap_angle = math.radians(scn.unwrapAngle)
        
        # Store original mode
        original_mode = bpy.context.mode
        
        # Make sure we're in object mode to start
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        # Deselect all first
        bpy.ops.object.select_all(action='DESELECT')
        
        # Mark edges for all objects if using seam/sharp
        if use_seam_sharp:
            for obj in objects:
                if obj.type == "MESH":
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='OBJECT')
                    self.mark_edges_for_unwrap(obj)
        
        # Select all mesh objects
        mesh_objects = [obj for obj in objects if obj.type == "MESH"]
        for obj in mesh_objects:
            obj.select_set(True)
        
        if not mesh_objects:
            return 0
        
        bpy.context.view_layer.objects.active = mesh_objects[0]
        
        # Enter edit mode with all objects
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Unwrap
        if use_seam_sharp:
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
        else:
            bpy.ops.uv.smart_project(
                angle_limit=unwrap_angle,
                island_margin=0.001, 
                area_weight=0.0, 
                correct_aspect=True,
                scale_to_bounds=False)
        
        # Exit edit mode before applying texel density
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Apply texel density if enabled
        if scn.useTexelDensity:
            self.apply_texel_density(mesh_objects)
        
        return len(mesh_objects)
    
    def apply_texel_density(self, objects):
        """Apply uniform texel density across all objects"""
        scn = bpy.context.scene
        texture_size = int(scn.textureResolution)
        
        # Get texel density and convert to pixels per meter
        if scn.texelDensityUnit == 'PX_M':
            texel_density = float(scn.texelDensityPresetMeters)
        else:  # PX_CM
            texel_density = float(scn.texelDensityPresetCentimeters) * 100.0  # Convert px/cm to px/m
        
        for obj in objects:
            if obj.type != 'MESH':
                continue
            
            # Make sure we're in object mode
            if bpy.context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
                
            bpy.context.view_layer.objects.active = obj
            
            # Get mesh data
            mesh = obj.data
            if not mesh.uv_layers or not mesh.uv_layers.active:
                continue
            
            # Force update mesh data
            mesh.update()
            
            uv_layer = mesh.uv_layers.active.data
            
            # Check if UV layer has data
            if len(uv_layer) == 0:
                continue
            
            # Calculate 3D surface area
            bm = bmesh.new()
            bm.from_mesh(mesh)
            bm.faces.ensure_lookup_table()
            
            surface_area_3d = sum(face.calc_area() for face in bm.faces)
            bm.free()
            
            if surface_area_3d <= 0:
                continue
            
            # Calculate UV area
            uv_area = 0.0
            for poly in mesh.polygons:
                # Get UV coordinates for this polygon
                uv_coords = []
                for loop_index in poly.loop_indices:
                    uv_coords.append(uv_layer[loop_index].uv[:])
                
                # Calculate UV polygon area using shoelace formula
                if len(uv_coords) >= 3:
                    area = 0.0
                    for i in range(len(uv_coords)):
                        j = (i + 1) % len(uv_coords)
                        area += uv_coords[i][0] * uv_coords[j][1]
                        area -= uv_coords[j][0] * uv_coords[i][1]
                    uv_area += abs(area) * 0.5
            
            if uv_area <= 0:
                continue
            
            # Correct Texel Density formula:
            # Texel Density (pixels/meter) = Texture Width (pixels) × √(UV Area / 3D Surface Area in m²)
            # 
            # To achieve target texel density:
            # target_TD = texture_size × √(UV_area / 3D_area)
            # Solve for new UV_area:
            # target_TD / texture_size = √(new_UV_area / 3D_area)
            # (target_TD / texture_size)² = new_UV_area / 3D_area
            # new_UV_area = 3D_area × (target_TD / texture_size)²
            # 
            # Scale factor = √(new_UV_area / current_UV_area)
            
            current_texel_density = texture_size * math.sqrt(uv_area / surface_area_3d)
            scale_factor = texel_density / current_texel_density
            
            # Scale all UV coordinates from origin (0, 0)
            for poly in mesh.polygons:
                for loop_index in poly.loop_indices:
                    uv = uv_layer[loop_index].uv
                    uv_layer[loop_index].uv = (uv[0] * scale_factor, uv[1] * scale_factor)
            
            # Update mesh
            mesh.update()

    def execute(self, context):
        selection = bpy.context.selected_objects
        
        # If no objects selected but in edit mode, get the active object
        if len(selection) == 0 and context.mode == 'EDIT_MESH':
            if context.active_object and context.active_object.type == 'MESH':
                selection = [context.active_object]
        
        if len(selection) == 0:
            self.report({'WARNING'}, "No mesh objects selected")
            return {'CANCELLED'}
        
        use_seam_sharp = bpy.context.scene.sharp or bpy.context.scene.seam
        
        # Batch unwrap all objects together
        amt = self.batch_unwrap(selection, use_seam_sharp)
        
        # Reselect all objects
        for obj in selection:
            if obj.type == "MESH":
                obj.select_set(True)
        
        if amt > 0:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            
            message = f"Unwrapped {amt} object(s) at {bpy.context.scene.unwrapAngle}° angle"
            if bpy.context.scene.useTexelDensity:
                if bpy.context.scene.texelDensityUnit == 'PX_M':
                    td_value = float(bpy.context.scene.texelDensityPresetMeters)
                    message += f" with {td_value:.2f} px/m texel density"
                else:
                    td_value = float(bpy.context.scene.texelDensityPresetCentimeters)
                    message += f" with {td_value:.2f} px/cm texel density"
            
            self.report({'INFO'}, message)
        else:
            self.report({'WARNING'}, "No mesh objects selected")
        
        return {'FINISHED'}

class DARROW_MT_modelingPie(Menu):
    bl_label = "Modeling Tools"

    def draw(self, context):
        layout = self.layout

        objs = context.selected_objects
        all = bpy.data.objects

        if len(all) != 0:
            if context.mode == 'OBJECT':
                prnt = layout.row()
                cf = prnt.row().menu_pie()
                cf.operator('move.origin', text="Origin",icon="TRANSFORM_ORIGINS")
                cf.operator('cleanup.mesh', text = "Cleanup", icon="VERTEXSEL")

                box = cf.box().column(align=True)
                box.scale_y = 1.33
                col = box.row(align=True).split(align=True, factor=0.67)
                Var_displayBool = bpy.context.scene.vertexDisplayBool
                col.prop(context.scene, "colorPicker", text="")
                col.operator('set.display', icon="HIDE_OFF",text="", depress=Var_displayBool)
                if len(objs) == 0:
                    col.enabled = False

                smooth = cf.box().row(align=True).split(align=True)
                smooth.scale_y = 1.33
                smooth.operator('shade.smooth', text = "Smooth",icon="MOD_SMOOTH")
                smooth.operator('shade.sharp', text="Sharp", icon="MOD_NOISE")

                cf.operator("unwrap.selected", text="Unwrap", icon="UV")
                cf.operator('apply.transforms', text="Transforms",icon="OBJECT_ORIGIN")
                cf.operator('apply.normals', text="Normals", icon="ORIENTATION_NORMAL")
                cf.operator('darrow.move_on_grid', text="Align", icon="MOD_LATTICE")

                if len(objs) == 0:
                    cf.enabled = False
                else:
                    cf.enabled = True

class ModelingToolsPopUpCallback(bpy.types.Operator):
    bl_label = "Modeling Tools Popup"
    bl_idname = "darrow.modeling_tools_callback"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="DARROW_MT_modelingPie")
        return {'FINISHED'}

#-----------------------------------------------------#  
#   Registration classes
#-----------------------------------------------------#
classes = ( DarrowClearSharp,DarrowClearUVs, DarrowClearSeam, DarrowCleanupMesh,DarrowSharp,createOrient,DARROW_PT_toolPanel,DARROW_PT_toolExtendPanel, DARROW_PT_toolPanel_2, DARROW_PT_toolPanel_3, DARROW_PT_toolPanel_4,DARROW_PT_toolPanel_5, DARROW_PT_toolPanel_6,DARROW_PT_toolPanel_7, DARROW_PT_toolPanel_8, DARROW_PT_toolPanel_LOD, CTO_OT_Dummy, DarrowClearOrientation, DarrowSetOrigin, DarrowMoveOrigin, DarrowTransforms, DarrowNormals, DarrowSmooth, DarrowSetIsCutter, DarrowSetStaticBevel, DarrowGenerateLODs,
           DarrowCircleArray, DarrowClearSelected, DarrowSetBlack, DarrowSetWhite, DarrowSetRed, DarrowSetGreen, DarrowSetBlue, DarrowSetColor, DarrowSetDisplay,DarrowUnwrapSelected,DarrowMoveOnGrid, DARROW_MT_modelingPie, ModelingToolsPopUpCallback)

addon_keymaps = []

def register():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(ModelingToolsPopUpCallback.bl_idname, 'E', 'PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.sharp = bpy.props.BoolProperty(
        name="Mark Sharp",
        description="When unwrapping, mark angled edges as sharp",
        default=True
    )
    bpy.types.Scene.seam = bpy.props.BoolProperty(
        name="Mark Seam",
        description="When unwrapping, mark angled edges as seam",
        default=True
    )

    bpy.types.Scene.colorPicker = bpy.props.FloatVectorProperty(
        name = "Color Picker",
        subtype = "COLOR",
        min = 0.0,
        max = 1.0,
        size = 3,
        default = (1.0,1.0,1.0),
        update=UpdateVertColor
    )

    bpy.types.Scene.alignGridHeight = bpy.props.FloatProperty(
        name = "Grid Height Offset",
        default=0,
        step=1,
        soft_max=50,
        soft_min=0,
    )

    bpy.types.Scene.alignGridRows = bpy.props.IntProperty(
        name = "Rows",
        default=2,
        step=1,
        soft_max=10,
        soft_min=1
    )

    bpy.types.Scene.alignGridSpacing = bpy.props.FloatProperty(
        name = "Spacing",
        default=15,
        soft_max=50,
        soft_min=1
    )

    bpy.types.Scene.unwrapAngle = bpy.props.IntProperty(
        name = "Int",
        default = 66,
        min = 0,
        max = 89,
        step = 1,
        update = updateSharpSeam
    )

    bpy.types.Scene.useTexelDensity = bpy.props.BoolProperty(
        name="Use Texel Density",
        description="Apply uniform texel density when unwrapping",
        default=False
    )

    bpy.types.Scene.texelDensityUnit = bpy.props.EnumProperty(
        name="Texel Density Unit",
        description="Unit for texel density measurement",
        items=[
            ('PX_M', "px/m", "Pixels per meter"),
            ('PX_CM', "px/cm", "Pixels per centimeter"),
        ],
        default='PX_CM'
    )

    bpy.types.Scene.textureResolution = bpy.props.EnumProperty(
        name="Texture Resolution",
        description="Target texture resolution",
        items=[
            ('512', "512", "512x512"),
            ('1024', "1K (1024)", "1024x1024"),
            ('2048', "2K (2048)", "2048x2048"),
            ('4096', "4K (4096)", "4096x4096"),
            ('8192', "8K (8192)", "8192x8192"),
        ],
        default='2048'
    )

    bpy.types.Scene.texelDensityPresetMeters = bpy.props.EnumProperty(
        name="Texel Density (px/m)",
        description="Texel density in pixels per meter",
        items=[
            ('10.24', "10.24 px/m", "Very low detail - Large background objects"),
            ('20.48', "20.48 px/m", "Low detail - Background objects"),
            ('40.96', "40.96 px/m", "Medium-low detail"),
            ('81.92', "81.92 px/m", "Medium detail"),
            ('163.84', "163.84 px/m", "Medium-high detail"),
            ('256', "256 px/m", "High detail"),
            ('512', "512 px/m", "Very high detail"),
            ('1024', "1024 px/m", "Extreme detail - Hero objects"),
            ('2048', "2048 px/m", "Ultra detail"),
            ('4096', "4096 px/m", "Maximum detail"),
        ],
        default='256'
    )

    bpy.types.Scene.texelDensityPresetCentimeters = bpy.props.EnumProperty(
        name="Texel Density (px/cm)",
        description="Texel density in pixels per centimeter",
        items=[
            ('0.512', "0.51 px/cm", "Very low detail - Large background objects"),
            ('1.024', "1.02 px/cm", "Low detail - Background objects"),
            ('2.048', "2.05 px/cm", "Medium-low detail"),
            ('2.56', "2.56 px/cm", "Medium detail"),
            ('4.096', "4.10 px/cm", "Medium-high detail"),
            ('8.192', "8.19 px/cm", "High detail"),
            ('10.24', "10.24 px/cm", "Very high detail"),
            ('20.48', "20.48 px/cm", "Extreme detail - Hero objects"),
            ('40.96', "40.96 px/cm", "Ultra detail"),
            ('81.92', "81.92 px/cm", "Maximum detail"),
        ],
        default='2.56'
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
        default = 0.01,
        soft_min = 0.00001,
        soft_max = 0.5,
        step = 0.01,
    )
    
    bpy.types.Scene.fixNgons = bpy.props.BoolProperty(
        name = "Tris to quads",
        default = False
    )

    # LOD Generator Properties
    bpy.types.Scene.lodCount = bpy.props.IntProperty(
        name="LOD Count",
        description="Number of LOD levels to generate",
        default=4,
        min=2,
        max=6
    )

    bpy.types.Scene.lodFinalType = bpy.props.EnumProperty(
        name="Final LOD Type",
        description="Type of geometry for the final (lowest) LOD",
        items=[
            ('BBOX', "Bounding Box", "Simple box matching object bounds"),
            ('CONVEX', "Convex Hull", "Convex hull wrapping the object"),
        ],
        default='BBOX'
    )

    bpy.types.Scene.lodPreserveUVs = bpy.props.BoolProperty(
        name="Preserve UVs",
        description="Try to preserve UV coordinates during decimation",
        default=True
    )

    bpy.types.Scene.lodKeepMaterials = bpy.props.BoolProperty(
        name="Keep Materials",
        description="Copy materials to all LOD levels",
        default=True
    )

    bpy.types.Scene.lodTriangulate = bpy.props.BoolProperty(
        name="Triangulate",
        description="Convert all faces to triangles (for game engine export)",
        default=False
    )

    bpy.types.Scene.lodApplyModifiers = bpy.props.BoolProperty(
        name="Apply Modifiers",
        description="Apply all modifiers before combining meshes",
        default=True
    )

    bpy.types.Scene.lodShadeSmooth = bpy.props.BoolProperty(
        name="Shade Smooth",
        description="Apply smooth shading to generated LODs",
        default=True
    )

    bpy.types.Scene.lodSmartUnbevel = bpy.props.BoolProperty(
        name="Smart Un-Bevel",
        description="Reduce all bevel modifiers to 1 segment before LOD generation (includes boolean cutters)",
        default=False
    )

    # LOD Decimation Ratios (per-scene, shown dynamically in panel)
    bpy.types.Scene.lodRatio1 = bpy.props.FloatProperty(
        name="LOD1 Ratio",
        description="Decimation ratio for LOD1 (1.0 = 100%)",
        default=0.5,
        min=0.01,
        max=1.0,
        precision=2
    )
    bpy.types.Scene.lodRatio2 = bpy.props.FloatProperty(
        name="LOD2 Ratio",
        description="Decimation ratio for LOD2 (1.0 = 100%)",
        default=0.25,
        min=0.01,
        max=1.0,
        precision=2
    )
    bpy.types.Scene.lodRatio3 = bpy.props.FloatProperty(
        name="LOD3 Ratio",
        description="Decimation ratio for LOD3 (1.0 = 100%)",
        default=0.125,
        min=0.01,
        max=1.0,
        precision=2
    )
    bpy.types.Scene.lodRatio4 = bpy.props.FloatProperty(
        name="LOD4 Ratio",
        description="Decimation ratio for LOD4 (1.0 = 100%)",
        default=0.0625,
        min=0.01,
        max=1.0,
        precision=2
    )
    bpy.types.Scene.lodRatio5 = bpy.props.FloatProperty(
        name="LOD5 Ratio",
        description="Decimation ratio for LOD5 (1.0 = 100%)",
        default=0.03,
        min=0.01,
        max=1.0,
        precision=2
    )

def unregister():
    bpy.types.VIEW3D_PT_transform_orientations.remove(extend_transfo_pop_up)
    
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()