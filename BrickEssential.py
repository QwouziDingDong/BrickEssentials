bl_info = {
    "name": "BrickEssential (by Qwouzi)",
    "description": "Full tutorial on my youtube channel https://www.youtube.com/@Qwouzi",
    "author": "Qwouzi",
    "version": (0, 5, 8),
    "blender": (4, 2, 0),
    "location": "3D View > Tools",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}


import bpy
import math
import mathutils
import os
import random
import bmesh
import random
import time
from mathutils import Vector

from bpy.props import (EnumProperty,
                        StringProperty,
                        BoolProperty,
                        IntProperty,
                        PointerProperty,
                        )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class Properties(PropertyGroup):
    
    segments: IntProperty(
        name = "Segments",
        description="Segments the Strings are made of",
        default = 3,
        min = 2,
        max = 10
        )

    xbrick: IntProperty(
        name = "Width",
        description="Amount of studs that the brick is on the x axis",
        default = 1,
        min = 1,
        max = 99
        )
    ybrick: IntProperty(
        name = "Length",
        description="Amount of studs that the brick is on the y axis",
        default = 2,
        min = 1,
        max = 99
        )
    zbrick: IntProperty(
        name = "Height",
        description="Amount of plates that the brick is on the z axis",
        default = 3,
        min = 1,
        max = 99
        )
        
    house_type: EnumProperty(
        name="House Type",
        description="Select House Type",
        items=[ ("House 1", "House 1", ""),
                ("House 2", "House 2", ""),
                ("House 3", "House 3", ""),
                ("House 4", "House 4", ""),
               ]
        )
        
    blast_on_off: BoolProperty(
        name="Blast ON/OFF",
        description="Turn the shockwave On/Off",
        default = False
        )

    projectile_speed: IntProperty(
        name = "Projectile speed",
        description="The speed the projectile travels at",
        default = 5,
        min = 1,
        max = 10
        )
        
    projectile_lifetime: IntProperty(
        name = "Projectile lifetime",
        description="Amount of frames, the projectiles stays alive",
        default = 24,
        min = 1,
        max = 1024
        )


    blast1_obj: StringProperty(
        name="Blast Stage 1 Part",
        description="First stage shockwave",
        default="",
        maxlen=1024,
        )
        
    blast2_obj: StringProperty(
        name="Blast Stage 2 Part",
        description="Second stage shockwave. (keep empty if only one shockwave)",
        default="",
        maxlen=1024,
        )
        
        
    projectile_obj: StringProperty(
        name="Projectile Part",
        description="Projectile brick",
        default="",
        maxlen=1024,
        )
        
    pin_obj: StringProperty(
        name = "Pin Point",
        description="Choose a Point (any Object) from where you want the building animation to happen",
        default="",
        maxlen=1024,
        )
    
    brick_coll: StringProperty(
        name = "Bricks Collection",
        description="Choose the Collection with your Lego model in",
        default="",
        maxlen=1024,
        )
    
    hide_bricks: BoolProperty(
        name = "Hide Before Building",
        description="If checked, bricks will be hidden until they spawn in to be build",
        default = False
        )
    
    build_speed: IntProperty(
        name = "Speed",
        description = "Speed, how fast the bricks are flying. (value = number of frames in the air)",
        default = 12,
        min = 1,
        max = 30
        )
    
    place_amount: IntProperty(
        name = "Amount",
        description = "Amount of bricks that get built at the same time. (higher value = faster building)",
        default = 1,
        min = 1,
        max = 30
        )
# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class Generate(Operator):
    bl_label = "Generate"
    bl_idname = "lb.generate"
    
    @classmethod
    def poll(self,context):
        return context.object is not None

    def execute(self, context):
        scene = context.scene
        tool = scene.tools
        
        
        obj = bpy.context.selected_objects[0]

        print(obj.data)
        
        is_gun = False
        
        if "62885" in obj.data.name:
            blast_rot = 1.25
            blast_loc = (0, 9.4, 8)
            
            wave_rot = (1.25, 0, 0)
            wave_loc = (0, 13.5, 10)
            
            is_gun = True
              
        if "87993" in obj.data.name:
            blast_rot = 1.25
            blast_loc = (0, 8.7, 8)
            
            wave_rot = (1.25, 0, 0)
            wave_loc = (0, 12.5, 10)
            
            is_gun = True
            
            
        if "95199" in obj.data.name:
            blast_rot = 1.1
            blast_loc = (0, 9.4, 8)
            
            wave_rot = (1.1, 0, 0)
            wave_loc = (0, 15.4, 9.5)
            
            is_gun = True
            
        if "15445" in obj.data.name:
            blast_rot = 1.57
            blast_loc = (0, 10, 18)
            
            wave_rot = (1.57, 0, 0)
            wave_loc = (0, 10.3, 22)
            
            is_gun = True
            
        if "2562" in obj.data.name:
            blast_rot = 1.57
            blast_loc = (0, 0, 0)
            
            wave_rot = (1.57, 0, 0)
            wave_loc = (0, 0, 4)
            
            is_gun = True
            
        if "30132" in obj.data.name:
            blast_rot = 1.57
            blast_loc = (0, 3.2, 8)
            
            wave_rot = (1.57, 0, 0)
            wave_loc = (0, 3.2, 10.4)
            
            is_gun = True
        
        if "85973" in obj.data.name:
            blast_rot = 1.25
            blast_loc = (0, 9.75, 18)
            
            wave_rot = (1.25, 0, 0)
            wave_loc = (0, 16.8, 19.8)
            
            is_gun = True
            
        if "24144" in obj.data.name:
            blast_rot = 1.15
            blast_loc = (0, 9.5, 10)
            
            wave_rot = (1.15, 0, 0)
            wave_loc = (0, 15.4, 11.1)
            
            is_gun = True
            
        if "92738" in obj.data.name:
            blast_rot = 1.35
            blast_loc = (0, 7.65, 2)
            
            wave_rot = (1.35, 0, 0)
            wave_loc = (0, 9.8, 8.6)
            
            is_gun = True
            
        if "58247" in obj.data.name:
            blast_rot = 1.35
            blast_loc = (0, 8, 8)
            
            wave_rot = (1.35, 0, 0)
            wave_loc = (0, 10.1, 8.6)
            
            is_gun = True
        
        if "57899" in obj.data.name:
            blast_rot = 1.35
            blast_loc = (0, 8.75, 16)
            
            wave_rot = (1.35, 0, 0)
            wave_loc = (0, 13.6, 20.9)
            
            is_gun = True
            
        if "4360" in obj.data.name:
            blast_rot = 1.57
            blast_loc = (0, 5.9, 0)
            
            wave_rot = (1.57, 0, 0)
            wave_loc = (0, 5.8, 10)
            
            is_gun = True
            
                
            
            

        if is_gun == True:
        #Add and transform blast object
            blast = bpy.context.scene.objects[tool.projectile_obj].copy()
            blast.data = bpy.context.scene.objects[tool.projectile_obj].data.copy()
            bpy.context.collection.objects.link(blast)
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = blast
            
            bpy.ops.object.rotation_clear(clear_delta=False)
            bpy.ops.object.location_clear(clear_delta=False) 
            
            blast.rotation_euler = (1.57, 0, 0)
            blast.location = blast_loc
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            blast.data.transform(blast.matrix_world)
            
            constraint = blast.constraints.new(type='COPY_ROTATION')
            constraint.target = obj
            bpy.ops.constraint.apply(constraint="Copy Rotation", owner='OBJECT')
            
            constraint2 = blast.constraints.new(type='COPY_LOCATION')
            constraint2.target = obj
            bpy.ops.constraint.apply(constraint="Copy Location", owner='OBJECT')
            
            
            blast.rotation_euler = (blast.rotation_euler.x + blast_rot - 1.57, blast.rotation_euler.y, blast.rotation_euler.z)
                
            
        #Add GeometryNode system
            modifier = blast.modifiers.new(type='NODES', name='Shooting Speed')
            
            bpy.ops.node.new_geometry_node_group_assign()
            node_group = bpy.context.object.modifiers[0].node_group
            
            nodes = node_group.nodes
            
            transform = nodes.new(type="GeometryNodeTransform")
            
            combineXYZ1 = nodes.new(type='ShaderNodeCombineXYZ')
            combineXYZ1.location.x -= 200
            combineXYZ1.location.y -= 100
            
            combineXYZ2 = nodes.new(type='ShaderNodeCombineXYZ')
            combineXYZ2.location.x -= 200
            combineXYZ2.location.y -= 200
            #combineXYZ2.inputs[0].default_value = blast_x_rot
            
            math = nodes.new(type="ShaderNodeMath")
            math.operation = 'MULTIPLY'
            math.inputs[1].default_value = (tool.projectile_speed / 10 + 0.5) * 26
            math.location.x -= 400
            math.location.y -= 200
            
            math2 = nodes.new(type="ShaderNodeMath")
            math2.operation = 'MULTIPLY'
            #math2.inputs[1].default_value = speed = ((tool.projectile_speed / 10 + 0.5) * blast_speed_y)
            math2.location.y -= 400
            
            math3 = nodes.new(type="ShaderNodeMath")
            math3.operation = 'ADD'
            math3.inputs[1].default_value = 10.25
            math3.location.x -= 400
            math3.location.y -= 600
            
            math4 = nodes.new(type="ShaderNodeMath")
            math4.operation = 'ADD'
            math4.inputs[1].default_value = 0.5
            math4.location.x -= 600
            math4.location.y -= 200


            value = nodes.new(type="ShaderNodeValue")
            v = value.outputs[0].driver_add("default_value")
            frame_i = bpy.data.scenes[0].frame_current
            frame_s = str(frame_i - 1)
            v.driver.expression = "frame - " + frame_s
            value.location.x -= 800
            value.location.y -= 200
            
            group_in = nodes.get('Group Input')
            
            group_out = nodes.get('Group Output')
            
        #Linking nodes together
            node_group.links.new(group_in.outputs['Geometry'], transform.inputs['Geometry'])
            node_group.links.new(transform.outputs['Geometry'], group_out.inputs['Geometry'])
            node_group.links.new(combineXYZ1.outputs['Vector'], transform.inputs['Translation'])
            node_group.links.new(combineXYZ2.outputs['Vector'], transform.inputs['Rotation'])
            node_group.links.new(math2.outputs['Value'], math3.inputs['Value'])
            #node_group.links.new(math3.outputs['Value'], combineXYZ1.inputs['Y'])
            node_group.links.new(math.outputs['Value'], combineXYZ1.inputs['Z'])
            node_group.links.new(value.outputs['Value'], math4.inputs['Value'])
            node_group.links.new(math4.outputs['Value'], math2.inputs['Value'])
            node_group.links.new(math4.outputs['Value'], math.inputs['Value'])
            
        #Add keyframes for appearing
            bpy.data.scenes['Scene'].frame_set(frame_i)
            blast.hide_render = False
            blast.keyframe_insert(data_path="hide_render")
            blast.hide_viewport = False
            blast.keyframe_insert(data_path="hide_viewport")
            
            bpy.data.scenes['Scene'].frame_set(frame_i - 1)
            blast.hide_render = True
            blast.keyframe_insert(data_path="hide_render")
            blast.hide_viewport = True
            blast.keyframe_insert(data_path="hide_viewport")
            
            bpy.data.scenes['Scene'].frame_set(frame_i + tool.projectile_lifetime)
            blast.hide_render = True
            blast.keyframe_insert(data_path="hide_render")
            blast.hide_viewport = True
            blast.keyframe_insert(data_path="hide_viewport")
            
            bpy.data.scenes['Scene'].frame_set(frame_i)
            
#--------------------------------------------------------------------------        
#   Adding Shockwave Piece
# -------------------------------------------------------------------------
            
            if tool.blast_on_off == True:  
                #bpy.data.scenes['Scene'].frame_set(frame_i)    
                
                offset = 0
                if tool.blast2_obj != "":
                    offset = 1
                      
                    bpy.data.scenes['Scene'].frame_set(frame_i)  
                    wave2 = bpy.context.scene.objects[tool.blast2_obj].copy()
                    wave2.data = bpy.context.scene.objects[tool.blast2_obj].data.copy()
                    bpy.context.collection.objects.link(wave2)
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = bpy.data.objects[wave2.name]
                    
                    wave2.rotation_euler = wave_rot
                    wave2.location = wave_loc
                    
                    bpy.ops.object.transform_apply(rotation=True)
                    wave2.data.transform(wave2.matrix_world)
                    
                    constraint = wave2.constraints.new(type='COPY_ROTATION')
                    constraint.target = obj
                    bpy.ops.constraint.apply(constraint="Copy Rotation", owner='OBJECT')
                    
                    constraint2 = wave2.constraints.new(type='COPY_LOCATION')
                    constraint2.target = obj
                    bpy.ops.constraint.apply(constraint="Copy Location", owner='OBJECT')        

                    #Add keyframes for appearing
                    bpy.data.scenes['Scene'].frame_set(frame_i)
                    wave2.hide_render = False
                    wave2.keyframe_insert(data_path="hide_render")
                    wave2.hide_viewport = False
                    wave2.keyframe_insert(data_path="hide_viewport")
                    
                    bpy.data.scenes['Scene'].frame_set(frame_i + 1)
                    wave2.hide_render = True
                    wave2.keyframe_insert(data_path="hide_render")
                    wave2.hide_viewport = True
                    wave2.keyframe_insert(data_path="hide_viewport")
                    
                    bpy.data.scenes['Scene'].frame_set(frame_i - 1)
                    wave2.hide_render = True
                    wave2.keyframe_insert(data_path="hide_render")
                    wave2.hide_viewport = True
                    wave2.keyframe_insert(data_path="hide_viewport")
                      
#----------------------------------------------------------------------------                      
#  Shockwave second stage
#----------------------------------------------------------------------------   
                bpy.data.scenes['Scene'].frame_set(frame_i + offset)                                  
                wave1 = bpy.context.scene.objects[tool.blast1_obj].copy()
                wave1.data = bpy.context.scene.objects[tool.blast1_obj].data.copy()
                bpy.context.collection.objects.link(wave1)
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = bpy.data.objects[wave1.name]
                
                wave1.rotation_euler = wave_rot
                wave1.location = wave_loc
                
                bpy.ops.object.transform_apply(rotation=True)
                wave1.data.transform(wave1.matrix_world)
                
                constraint = wave1.constraints.new(type='COPY_ROTATION')
                constraint.target = obj
                bpy.ops.constraint.apply(constraint="Copy Rotation", owner='OBJECT')
                
                constraint2 = wave1.constraints.new(type='COPY_LOCATION')
                constraint2.target = obj
                bpy.ops.constraint.apply(constraint="Copy Location", owner='OBJECT')        

                #Add keyframes for appearing
                bpy.data.scenes['Scene'].frame_set(frame_i + offset )
                wave1.hide_render = False
                wave1.keyframe_insert(data_path="hide_render")
                wave1.hide_viewport = False
                wave1.keyframe_insert(data_path="hide_viewport")
                
                bpy.data.scenes['Scene'].frame_set(frame_i + 1 + offset)
                wave1.hide_render = True
                wave1.keyframe_insert(data_path="hide_render")
                wave1.hide_viewport = True
                wave1.keyframe_insert(data_path="hide_viewport")
                
                bpy.data.scenes['Scene'].frame_set(frame_i - 1)
                wave1.hide_render = True
                wave1.keyframe_insert(data_path="hide_render")
                wave1.hide_viewport = True
                wave1.keyframe_insert(data_path="hide_viewport")
    
    
    
    
        else:
            print("false")
        
        
        return {'FINISHED'}
    
class AddWeb(Operator):
    bl_label = "Add Web"
    bl_idname = "lb.addweb"

    def execute(self, context):
        scene = context.scene
        tool = scene.tools

        filepath = os.path.dirname(os.path.abspath(__file__))

        filepath = os.path.join(filepath, "BrickEssentials", "StringRigs.blend")
        
        if "Web" in bpy.data.collections:
            bpy.data.collections["Web"].name = "Web_old"
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.collections = ["Web"]
            
        bpy.context.scene.collection.children.link(bpy.data.collections["Web"])

        
        for obj in bpy.data.collections.get("Web").objects:
            if obj.type == 'CURVE':
            # Return the only curve object in the collection
        
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj

                bpy.ops.object.mode_set(mode='EDIT')

                bpy.ops.curve.select_all(action='SELECT')
                bpy.ops.curve.delete(type='VERT')

                m = tool.segments;

                for i in range(m):
                    bpy.ops.curve.vertex_add(location=(i * 50, 0, 0))
                    bpy.ops.object.hook_add_newob()
                    
                    bpy.ops.object.mode_set(mode='OBJECT')

                    empty = bpy.context.selected_objects[0]
                    empty.users_collection[0].objects.unlink(empty)
                    bpy.data.collections["Web"].objects.link(empty)
                    
                        
                    empty.empty_display_type = 'SPHERE'
                    
                    bpy.ops.transform.resize(value=(5, 5, 5))
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    bpy.ops.object.mode_set(mode='EDIT')

                bpy.ops.curve.select_all(action='SELECT')
                bpy.ops.curve.handle_type_set(type='ALIGNED')

                bpy.ops.object.mode_set(mode='OBJECT')
      
        return {'FINISHED'}

class AddChain(Operator):
    bl_label = "Add Chain"
    bl_idname = "lb.addchain"

    def execute(self, context):
        scene = context.scene
        tool = scene.tools

        filepath = os.path.dirname(os.path.abspath(__file__))

        filepath = os.path.join(filepath, "BrickEssentials", "StringRigs.blend")
        
        if "Chain" in bpy.data.collections:
            bpy.data.collections["Chain"].name = "Chain_old"
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.collections = ["Chain"]
            
        bpy.context.scene.collection.children.link(bpy.data.collections["Chain"])

        
        for obj in bpy.data.collections.get("Chain").objects:
            if obj.type == 'CURVE':
            # Return the only curve object in the collection
        
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj

                bpy.ops.object.mode_set(mode='EDIT')

                bpy.ops.curve.select_all(action='SELECT')
                bpy.ops.curve.delete(type='VERT')

                m = tool.segments;

                for i in range(m):
                    bpy.ops.curve.vertex_add(location=(i * 50, 0, 0))
                    bpy.ops.object.hook_add_newob()
                    
                    bpy.ops.object.mode_set(mode='OBJECT')

                    empty = bpy.context.selected_objects[0]
                    empty.users_collection[0].objects.unlink(empty)
                    bpy.data.collections["Chain"].objects.link(empty)
                    
                        
                    empty.empty_display_type = 'SPHERE'
                    
                    bpy.ops.transform.resize(value=(5, 5, 5))
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    bpy.ops.object.mode_set(mode='EDIT')

                bpy.ops.curve.select_all(action='SELECT')
                bpy.ops.curve.handle_type_set(type='ALIGNED')

                bpy.ops.object.mode_set(mode='OBJECT')
        
        
        
        return {'FINISHED'}
    
class AddHouse(Operator):
    bl_label = "Add House"
    bl_idname = "lb.addhouse"
    

    def execute(self, context):  
        scene = context.scene
        tool = scene.tools
        
        filepath = os.path.dirname(os.path.abspath(__file__))

        filepath = os.path.join(filepath, "BrickEssentials", "HouseRender.blend")
        
        if tool.house_type in bpy.data.collections:
            bpy.data.collections[tool.house_type].name = "House_old"
        
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.collections = [tool.house_type]
        
        bpy.context.scene.collection.children.link(bpy.data.collections[tool.house_type])
        
        
        return {'FINISHED'}
        
class AddClaw(Operator):
    bl_label = "Add doc. Ock's arms"
    bl_idname = "lb.addclaw"

    def execute(self, context):
        scene = context.scene
        
        filepath = os.path.dirname(os.path.abspath(__file__))

        filepath = os.path.join(filepath, "BrickEssentials", "StringRigs.blend")
        
        if "Claw" in bpy.data.collections:
            bpy.data.collections["Claw"].name = "Claw_old"
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.collections = ["Claw"]

        bpy.context.scene.collection.children.link(bpy.data.collections["Claw"])
        
        
        
        return {'FINISHED'}
    
class AddMinifig(Operator):
    bl_label = "Add Minifig to Collection"
    bl_idname = "lb.addminifig"
    
    @classmethod
    def poll(self,context):
        return context.object is not None

    def execute(self, context):
        scene = context.scene
        
        coll =  bpy.data.collections.new("Figure")
        bpy.data.collections['CrowdMinifigs'].children.link(coll)
        
        for obj in bpy.context.selected_objects:
            obj.users_collection[0].objects.unlink(obj)
            coll.objects.link(obj)
            
        
        
        
        return {'FINISHED'}
    
class AddCrowdNodes(Operator):
    bl_label = "Add Crowd Nodes"
    bl_idname = "lb.addcrowdnodes"

    def execute(self, context):
        scene = context.scene
        
        filepath = os.path.dirname(os.path.abspath(__file__))

        filepath = os.path.join(filepath, "BrickEssentials", "CrowdNodes.blend")

        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.collections = ["CrowdNodes"]

        bpy.context.scene.collection.children.link(bpy.data.collections["CrowdNodes"])
        
        
        
        return {'FINISHED'}
    
class AnimateBuilding(Operator):
    bl_label = "Build"
    bl_idname = "lb.animatebuilding"

    def execute(self, context):
        scene = context.scene
        tool = scene.tools
        
        bcoll = bpy.data.collections[tool.brick_coll]
        bricks = []
        pin = bpy.data.objects[tool.pin_obj]
        unique_object_data = {}

        for obj in bcoll.all_objects:
            bricks.append(obj.name)       
        
        dist = []
            
        for x in range(0, len(bricks)):
            p1 = bpy.data.objects[bricks[x]].location
            p2 = pin.location
            ret= ((p2.x-p1.x)**2) + ((p2.y-p1.y)**2) + ((p2.z-p1.z)**2)
            ret=math.sqrt(ret)
                
            dist.append(ret)
        
        combined = list(zip(dist, bricks))
        combined.sort(key=lambda x: x[0])
        sorted_dist, sorted_bricks = zip(*combined)
        
        print(sorted_dist)
        print(sorted_bricks)
        
        t = bpy.context.scene.frame_current
        max_rotation = 40
        for y in range(0, len(bricks), tool.place_amount):
            pinloc = bpy.data.objects[tool.pin_obj].location
            for r in range(0, tool.place_amount):
                bpy.data.objects[bricks[y + r]].keyframe_insert(data_path="location", frame=t + tool.build_speed)
                bpy.data.objects[bricks[y + r]].keyframe_insert(data_path="rotation_euler", frame=t + tool.build_speed)
                bpy.context.scene.frame_set(t)
                bpy.data.objects[bricks[y + r]].matrix_world.translation = pinloc
                
                rot_x = math.radians(random.uniform(-max_rotation, max_rotation))
                rot_y = math.radians(random.uniform(-max_rotation, max_rotation))
                rot_z = math.radians(random.uniform(-max_rotation, max_rotation))
                current_rot = bpy.data.objects[bricks[y + r]].rotation_euler
                new_rot = (
                    current_rot[0] + rot_x,
                    current_rot[1] + rot_y,
                    current_rot[2] + rot_z
                )
                bpy.data.objects[bricks[y + r]].rotation_euler =  new_rot
                
                bpy.data.objects[bricks[y + r]].keyframe_insert(data_path="location", frame=t)
                bpy.data.objects[bricks[y + r]].keyframe_insert(data_path="rotation_euler", frame=t)
                if (tool.hide_bricks == True):
                    bpy.data.objects[bricks[y + r]].keyframe_insert(data_path="hide_viewport", frame=t)
                    bpy.data.objects[bricks[y + r]].keyframe_insert(data_path="hide_render", frame=t)
                    bpy.data.objects[bricks[y + r]].hide_viewport = True
                    bpy.data.objects[bricks[y + r]].hide_render = True
                    bpy.data.objects[bricks[y + r]].keyframe_insert(data_path="hide_viewport", frame=t - 1)
                    bpy.data.objects[bricks[y + r]].keyframe_insert(data_path="hide_render", frame=t - 1)
            t = t + 1
            
            

            
        
        print("Done!")

        return {'FINISHED'}
    
class AddBrickQL(Operator):
    bl_label = "Add Brick"
    bl_idname = "qq.addbrick"

    def execute(self, context):
        scene = context.scene
        tool = scene.tools
        
        obj = bpy.context.active_object
        
        if tool.xbrick <= tool.ybrick:
            if "Reference Bricks" not in bpy.data.collections:
                bricks_collection = bpy.data.collections.new("Reference Bricks")
                bpy.context.scene.collection.children.link(bricks_collection)
            
            obj.users_collection[0].objects.unlink(bpy.context.active_object)
            bpy.data.collections["Reference Bricks"].objects.link(obj)

            bpy.data.collections["Reference Bricks"].hide_render = True
            if tool.xbrick < 10:  
                xb = "0" + str(tool.xbrick)
            else:
                xb = str(tool.xbrick)
            if tool.ybrick < 10:  
                yb = "0" + str(tool.ybrick)
            else:
                yb = str(tool.ybrick)
            if tool.zbrick < 10:  
                zb = "0" + str(tool.zbrick)
            else:
                zb = str(tool.zbrick)
            obj.name = xb + yb + zb
            #bpy.data.collections["Reference Bricks"].hide_viewport = True
        else:
            show_error("Don't be as silly as ItsAMeMozzarelli ☺")
            
        
        return {'FINISHED'}
    
class GenerateQL(Operator):
    bl_label = "Generate"
    bl_idname = "qq.generate"

    def execute(self, context):
        scene = context.scene
        tool = scene.tools
        start_time = time.time()

        def create_blocks_in_grid(obj, block_size):

            # Calculate the number of blocks in each dimension
            block_count_x = math.ceil(obj.dimensions.x / 8)
            block_count_y = math.ceil(obj.dimensions.y / 8)
            block_count_z = math.ceil(obj.dimensions.z / 3.2)

            # Loop through the grid of blocks
            arr=[]
            
            for x in range(block_count_x):
                for y in range(block_count_y):
                    for z in range(block_count_z):
                        # Calculate the position of the block
                        loc_x = x * 8 + 8 / 2 - (obj.dimensions.x / 2) + obj.location.x
                        loc_y = y * 8 + 8 / 2 - (obj.dimensions.y / 2) + obj.location.y
                        loc_z = z * 3.2 + 3.2 / 2 - (obj.dimensions.z / 2) + obj.location.z

                        arr.append(Vector((loc_x, loc_y, loc_z)))

            #bm.free()

            return arr

        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        selected_object = bpy.context.active_object


        block_size = 4
        arr = create_blocks_in_grid(selected_object, block_size)

        def is_inside(point, obj):
                _point = point - obj.location
                _, closest, nor, _ = obj.closest_point_on_mesh(_point)
                
                direction = closest - _point

                if direction.dot(nor) > 0:
                    return True
                else:
                    return False
                
        new_arr1 = []
        for point in arr:
            if is_inside(point, selected_object):
                new_arr1.append(point)

        arr = new_arr1


        coll = bpy.data.collections.new("- Subscribe to Qwouzi -")

        scene = bpy.context.scene
        scene.collection.children.link(coll)
        
        
        def b_count(obj_):
            brk_count = int(obj_.name[0] + obj_.name[1]) * int(obj_.name[2] + obj_.name[3]) * int(obj_.name[4] + obj_.name[5])
            return brk_count
        
        bricks_o = []
        bricks_v = []
        for brk in  bpy.data.collections.get("Reference Bricks").objects:
            if brk.name != "010101":
                if ".001" in brk.name:
                    print("test")
                else:
                    bricks_o.append(brk)
                    bricks_v.append(b_count(brk))
        
        combined = list(zip(bricks_o, bricks_v))
        combined.sort(key=lambda x: x[1], reverse=True)
        
        s_obj, s_val = zip(*combined)
        
        bricks_o = s_obj
        bricks_v = s_val
        
        for brk in bricks_o:
            offsets = [
                Vector((8 * i, 8 * j, 3.2 * k))
                for i in range(int(brk.name[0] + brk.name[1]))
                for j in range(int(brk.name[2] + brk.name[3]))
                for k in range(int(brk.name[4] + brk.name[5]))
            ]

            dots = []
            rem = []
            if 1 == 1:
                check_a = arr.copy()
                for point1 in arr:
                    matching_count = 0

                    # Iterate through the offsets
                    remove = []
                    for point_offset in offsets:
                        target_point = point1 + point_offset
                        if target_point in arr:
                            matching_count += 1
                            remove.append(target_point)

                    # Check if all points exist before performing an action
                    if matching_count == len(offsets):
                        dots.append(point1 + Vector(((int(brk.name[0] + brk.name[1]) - 1) * 4, 0, 0)) + Vector((0, (int(brk.name[2] + brk.name[3]) - 1) * 4, 0)))
                        
                        for k in remove:
                            #check_a.remove(k)
                            arr.remove(k)
                    """else:
                        for k in remove:
                            check_a.remove(k)"""
                        
            importer = bpy.ops.mesh.primitive_plane_add()
            
            
            bpy.data.collections["- Subscribe to Qwouzi -"].objects.link(bpy.context.object)
            bpy.context.object.users_collection[1].objects.unlink(bpy.context.active_object)
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.delete(type='VERT')
            bpy.ops.object.editmode_toggle()
            
            for p in dots:
                # Select the object to which you want to add a vertex
                obj = bpy.context.active_object

                new_vertex = (p)  # Replace with the coordinates of your new vertex

                # Add the new vertex to the object's vertices
                obj.data.vertices.add(1)
                obj.data.vertices[-1].co = new_vertex

                # Update the object to reflect the changes
                obj.data.update()
                    
                bpy.context.view_layer.update()
                
            #Add GeometryNode system
            modifier = bpy.context.active_object.modifiers.new(type='NODES', name='Shooting Speed')

            bpy.ops.node.new_geometry_node_group_assign()
            node_group = bpy.context.object.modifiers[0].node_group

            nodes = node_group.nodes

            instance = nodes.new(type='GeometryNodeInstanceOnPoints')
            instance.inputs[3].default_value = True
            instance.inputs[5].default_value[0] = 1.5708
            instance.inputs[5].default_value[2] = 1.5708
            instance.location.y -= 200


            obj_info = nodes.new(type='GeometryNodeObjectInfo')
            obj_info.location.x -= 200
            obj_info.location.y = 200
            obj_info.inputs[1].default_value = True
            obj_info.inputs[0].default_value = bpy.data.objects[brk.name]
            
            group_in = nodes.get('Group Input')

            group_out = nodes.get('Group Output')
            
            if brk.name + ".001" in bpy.data.objects:
                obj_info2 = nodes.new(type='GeometryNodeObjectInfo')
                obj_info2.location.x -= 200
                obj_info2.location.y = 0
                obj_info2.inputs[1].default_value = True
                obj_info2.inputs[0].default_value = bpy.data.objects[brk.name + ".001"]
                
                join_geo = nodes.new(type='GeometryNodeJoinGeometry')
                
                node_group.links.new(obj_info.outputs['Geometry'], join_geo.inputs['Geometry'])
                node_group.links.new(obj_info2.outputs['Geometry'], join_geo.inputs['Geometry'])
                node_group.links.new(join_geo.outputs['Geometry'], instance.inputs['Instance'])
            else:
                node_group.links.new(obj_info.outputs['Geometry'], instance.inputs['Instance'])
                

            #Linking nodes together
            node_group.links.new(group_in.outputs['Geometry'], instance.inputs['Points'])
            node_group.links.new(instance.outputs['Instances'], group_out.inputs['Geometry'])

            #--------------------------
            #Other Direction Check
            #--------------------------
            if int(brk.name[0] + brk.name[1]) < int(brk.name[2] + brk.name[3]):
                dots2 = []
                      
                check_a = arr.copy()
                offsets2 = [
                    Vector((8 * i, 8 * j, 3.2 * k))
                    for i in range(int(brk.name[2] + brk.name[3]))
                    for j in range(int(brk.name[0] + brk.name[1]))
                    for k in range(int(brk.name[4] + brk.name[5]))
                ]        
                for point1 in arr:
                    matching_count = 0

                    # Iterate through the offsets
                    remove = []
                    for point_offset in offsets2:
                        target_point = point1 + point_offset
                        if target_point in arr:
                            matching_count += 1
                            remove.append(target_point)

                    # Check if all points exist before performing an action
                    if matching_count == len(offsets2):
                        dots2.append(point1 + Vector(((int(brk.name[2] + brk.name[3]) - 1) * 4, 0, 0)) + Vector((0, (int(brk.name[0] + brk.name[1]) - 1) * 4, 0)))
                        for k in remove:
                            #check_a.remove(k) 
                            arr.remove(k)
                    """else:
                        for k in remove:
                            check_a.remove(k)  """   
                            
                importer2 = bpy.ops.mesh.primitive_plane_add()
                
                bpy.data.collections["- Subscribe to Qwouzi -"].objects.link(bpy.context.object)
                bpy.context.object.users_collection[1].objects.unlink(bpy.context.active_object)
            

                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.delete(type='VERT')
                bpy.ops.object.editmode_toggle()
                
                
                
                for p in dots2:
                    # Select the object to which you want to add a vertex
                    obj = bpy.context.active_object

                    new_vertex = (p)  # Replace with the coordinates of your new vertex

                    # Add the new vertex to the object's vertices
                    obj.data.vertices.add(1)
                    obj.data.vertices[-1].co = new_vertex

                    # Update the object to reflect the changes
                    obj.data.update()
                        
                    bpy.context.view_layer.update()
                    
                #Add GeometryNode system
                modifier = bpy.context.active_object.modifiers.new(type='NODES', name='Shooting Speed')

                bpy.ops.node.new_geometry_node_group_assign()
                node_group = bpy.context.object.modifiers[0].node_group

                nodes = node_group.nodes

                instance = nodes.new(type='GeometryNodeInstanceOnPoints')
                instance.inputs[3].default_value = True
                instance.inputs[5].default_value[0] = 1.5708
                instance.location.y -= 200


                obj_info = nodes.new(type='GeometryNodeObjectInfo')
                obj_info.location.x -= 200
                obj_info.location.y = 200
                obj_info.inputs[1].default_value = True
                obj_info.inputs[0].default_value = bpy.data.objects[brk.name]

                group_in = nodes.get('Group Input')

                group_out = nodes.get('Group Output')
                
                if brk.name + ".001" in bpy.data.objects:
                    obj_info2 = nodes.new(type='GeometryNodeObjectInfo')
                    obj_info2.location.x -= 200
                    obj_info2.location.y = 0
                    obj_info2.inputs[1].default_value = True
                    obj_info2.inputs[0].default_value = bpy.data.objects[brk.name + ".001"]
                    
                    join_geo = nodes.new(type='GeometryNodeJoinGeometry')
                    
                    node_group.links.new(obj_info.outputs['Geometry'], join_geo.inputs['Geometry'])
                    node_group.links.new(obj_info2.outputs['Geometry'], join_geo.inputs['Geometry'])
                    node_group.links.new(join_geo.outputs['Geometry'], instance.inputs['Instance'])
                else:
                    node_group.links.new(obj_info.outputs['Geometry'], instance.inputs['Instance'])
                    

                #Linking nodes together
                node_group.links.new(group_in.outputs['Geometry'], instance.inputs['Points'])
                node_group.links.new(instance.outputs['Instances'], group_out.inputs['Geometry'])
        #--------------
        #Fill with 1 by 1s
        #--------------
        
        dots3 = []
        if "010101" in bpy.data.objects:                
            for point in arr:   
                    dots3.append(point)
        
            importer3 = bpy.ops.mesh.primitive_plane_add()
            
            bpy.data.collections["- Subscribe to Qwouzi -"].objects.link(bpy.context.object)
            bpy.context.object.users_collection[1].objects.unlink(bpy.context.active_object)
            

            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.delete(type='VERT')
            bpy.ops.object.editmode_toggle()
            
            for p in dots3:
                # Select the object to which you want to add a vertex
                obj = bpy.context.active_object

                new_vertex = (p)  # Replace with the coordinates of your new vertex

                # Add the new vertex to the object's vertices
                obj.data.vertices.add(1)
                obj.data.vertices[-1].co = new_vertex

                # Update the object to reflect the changes
                obj.data.update()
                    
                bpy.context.view_layer.update()
                
            #Add GeometryNode system
            modifier = bpy.context.active_object.modifiers.new(type='NODES', name='Shooting Speed')

            bpy.ops.node.new_geometry_node_group_assign()
            node_group = bpy.context.object.modifiers[0].node_group

            nodes = node_group.nodes

            instance = nodes.new(type='GeometryNodeInstanceOnPoints')
            instance.inputs[3].default_value = True
            instance.inputs[5].default_value[0] = 1.5708
            instance.location.y -= 200


            obj_info = nodes.new(type='GeometryNodeObjectInfo')
            obj_info.location.x -= 200
            obj_info.location.y = 200
            obj_info.inputs[1].default_value = True
            obj_info.inputs[0].default_value = bpy.data.objects["010101"]

            group_in = nodes.get('Group Input')

            group_out = nodes.get('Group Output')
            
            if "010101.001" in bpy.data.objects:
                obj_info2 = nodes.new(type='GeometryNodeObjectInfo')
                obj_info2.location.x -= 200
                obj_info2.location.y = 0
                obj_info2.inputs[1].default_value = True
                obj_info2.inputs[0].default_value = bpy.data.objects["010101.001"]
                
                join_geo = nodes.new(type='GeometryNodeJoinGeometry')
                
                node_group.links.new(obj_info.outputs['Geometry'], join_geo.inputs['Geometry'])
                node_group.links.new(obj_info2.outputs['Geometry'], join_geo.inputs['Geometry'])
                node_group.links.new(join_geo.outputs['Geometry'], instance.inputs['Instance'])
            else:
                node_group.links.new(obj_info.outputs['Geometry'], instance.inputs['Instance'])
                

            #Linking nodes together
            node_group.links.new(group_in.outputs['Geometry'], instance.inputs['Points'])
            node_group.links.new(instance.outputs['Instances'], group_out.inputs['Geometry'])

        print("Brickalizer took", time.time() - start_time, " seconds to run")
        return {'FINISHED'}


def show_error(message):
    bpy.context.window_manager.popup_menu(
        lambda self, context: self.layout.label(text=message),
        title="Error!",
        icon='ERROR'
    )

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class LegoBlastPanel(Panel):
    bl_label = "BrickEssentials"
    bl_idname = "lb.panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "BrickEssentials"
    bl_context = "objectmode"   

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tool = scene.tools
        
        layout.label(text = "Subscribe to Qwouzi ")
        
        #---------
        #BrickHouse
        #---------
        
        layout.label(text = "")
        layout.label(text = "BrickHouse")
        layout.prop(tool, "house_type")
        layout.operator("lb.addhouse", icon="SNAP_VOLUME")
        
        #---------
        #Brickalizer
        #---------
        
        layout.label(text = "")
        layout.label(text = "Brickalizer")
        layout.prop(tool, "xbrick") 
        layout.prop(tool, "ybrick") 
        layout.prop(tool, "zbrick") 
        layout.operator("qq.addbrick", icon="OUTLINER")
        layout.operator("qq.generate", icon="MESH_GRID")
        
        #---------
        #Blasterizor
        #---------
        
        layout.label(text = "")
        layout.label(text = "Blasterizor:")
        layout.prop(tool, "blast_on_off")
        layout.prop(tool, "projectile_speed")
        layout.prop(tool, "projectile_lifetime")
        layout.prop(tool, "blast1_obj")
        layout.prop(tool, "blast2_obj")
        layout.prop(tool, "projectile_obj")
        layout.operator("lb.generate", icon= "TRACKER")
        
        #---------
        #BrickStrings
        #---------
        
        layout.label(text = "")
        layout.label(text = "BrickStrings:")
        layout.prop(tool, "segments")
        layout.operator("lb.addweb", icon= "OUTLINER_DATA_CURVE")
        layout.operator("lb.addchain", icon= "OUTLINER_DATA_CURVE")
        layout.operator("lb.addclaw", icon= "OUTLINER_DATA_CURVE")
        
        #---------
        #BrickCrowd
        #---------
        
        layout.label(text = "")
        layout.label(text = "BrickCrowd:")
        layout.operator("lb.addminifig", icon= "COMMUNITY")
        layout.operator("lb.addcrowdnodes", icon= "COMMUNITY")
        
        #---------
        #BrickBuilder
        #---------
        
        layout.label(text = "")
        layout.label(text = "BrickBuilder:")
        layout.prop(tool, "place_amount")
        layout.prop(tool, "build_speed")
        layout.prop(tool, "brick_coll")
        layout.prop(tool, "pin_obj")
        layout.prop(tool, "hide_bricks")
        layout.operator("lb.animatebuilding", icon= "SEQ_SEQUENCER")
        
        layout.separator()

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (

    Properties,
    Generate,
    AddWeb,
    AddChain,
    AddHouse,
    AddClaw,
    AddMinifig,
    AddCrowdNodes,
    AnimateBuilding,
    AddBrickQL,
    GenerateQL,
    LegoBlastPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.tools = PointerProperty(type=Properties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.tools


if __name__ == "__main__":
    register()