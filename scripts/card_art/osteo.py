"""OsteoTrack: a frosted-glass long bone with a fracture gap, wrapped by a soft cuff carrying a
vibration module and two small sensor pods. Illustrates the proposed concept; not a built device."""
import bpy, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from mathutils import Vector

out, W, H, SPP, F = args()
sc = reset(W, H, SPP, bg=(0.93, 0.94, 0.95), strength=0.45)

root = bpy.data.objects.new('root', None)
bpy.context.collection.objects.link(root)
root.rotation_euler = (0, 0, math.radians(-25) + F * 2 * math.pi)

# bone: lathe a profile (shaft with flared ends) around Z
prof = [(0.0, -1.62), (0.3, -1.6), (0.38, -1.48), (0.34, -1.3), (0.22, -1.05), (0.18, -0.7), (0.17, -0.06)]


def bone_half(sign, name):
    pts = [(r, sign * abs(z)) for r, z in prof]
    me = bpy.data.meshes.new(name)
    me.from_pydata([(r, 0, z) for r, z in pts], [(i, i + 1) for i in range(len(pts) - 1)], [])
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    sm = o.modifiers.new('lathe', 'SCREW')
    sm.angle = 2 * math.pi
    sm.steps = 96
    sm.render_steps = 96
    sm.use_merge_vertices = True
    sm.use_normal_calculate = True
    sm.use_normal_flip = sign > 0
    sub = o.modifiers.new('sub', 'SUBSURF')
    sub.levels = sub.render_levels = 2
    # cap the broken end
    for p in me.polygons:
        p.use_smooth = True
    o.parent = root
    return o


glass = mat('bone', (0.93, 0.89, 0.8), rough=0.55, coat=0.15)
glass.node_tree.nodes['Principled BSDF'].inputs['Subsurface Weight'].default_value = 0.3
glass.node_tree.nodes['Principled BSDF'].inputs['Subsurface Radius'].default_value = (0.1, 0.06, 0.04)
top = bone_half(1, 'top')
bot = bone_half(-1, 'bot')
for o in (top, bot):
    o.data.materials.append(glass)
top.rotation_euler = (0, math.radians(2.5), 0)
bot.rotation_euler = (0, math.radians(-1.5), 0)
# knobbly ends (condyles) so it reads as a bone
for zc in (1.62, -1.62):
    for xo in (-0.2, 0.2):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.27, location=(xo, 0, zc))
        kb = bpy.context.object
        smooth(kb)
        assign(kb, glass)
        kb.parent = top if zc > 0 else bot
# small glowing gap where the fracture is
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.165, depth=0.05, location=(0, 0, 0.0))
gap = bpy.context.object
smooth(gap)
assign(gap, emission('gap', (1.0, 0.45, 0.2), 3.0))
gap.parent = root

# cuff: a soft rounded band around the shaft just below the gap
bpy.ops.mesh.primitive_torus_add(major_radius=0.36, minor_radius=0.12, major_segments=128, minor_segments=32, location=(0, 0, -0.55))
cuff = bpy.context.object
cuff.scale = (1, 1, 2.6)
smooth(cuff)
assign(cuff, mat('cuff', (0.42, 0.55, 0.78), rough=0.5, sheen=0.6))
cuff.parent = root

# vibration module with contact disc, on the cuff's front
alu = mat('alu', (0.72, 0.73, 0.76), metal=1.0, rough=0.25)
slate = mat('slate', (0.06, 0.065, 0.075), rough=0.3, coat=0.8)
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.2, depth=0.12, location=(0, -0.5, -0.55), rotation=(math.pi / 2, 0, 0))
mod = bpy.context.object
smooth(mod, bevel=0.03, segments=6)
assign(mod, alu)
mod.parent = root
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.15, depth=0.02, location=(0, -0.565, -0.55), rotation=(math.pi / 2, 0, 0))
face = bpy.context.object
smooth(face, bevel=0.006, segments=3)
assign(face, slate)
face.parent = root
bpy.ops.mesh.primitive_torus_add(major_radius=0.155, minor_radius=0.005, major_segments=96, minor_segments=8, location=(0, -0.575, -0.55), rotation=(math.pi / 2, 0, 0))
led = bpy.context.object
assign(led, emission('led', (0.2, 0.5, 1.0), 6))
led.parent = root

# two sensor pods on thin strips, above and below the fracture
strip = mat('strip', (0.12, 0.13, 0.15), rough=0.5)
for z in (0.55, -1.25):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.205, minor_radius=0.018, major_segments=96, minor_segments=12, location=(0, 0, z))
    s = bpy.context.object
    s.scale = (1, 1, 1.6)
    smooth(s)
    assign(s, strip)
    s.parent = root
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0, -0.24, z))
    pod = bpy.context.object
    pod.scale = (0.14, 0.07, 0.1)
    bpy.ops.object.transform_apply(scale=True)
    smooth(pod, bevel=0.025, segments=5)
    assign(pod, slate)
    pod.parent = root

root.location = (0, 0, 2.0)
root.rotation_euler = (math.radians(0), math.radians(-30), root.rotation_euler[2])

floor = mat('floor', (0.88, 0.89, 0.91), rough=0.5, spec=0.3)
backdrop(floor, size=40, z=0.0)
flag = mat('flag', (0, 0, 0), rough=0.6, spec=0.0)
for fx, fy, rz in ((-3.2, 0.5, 70), (3.2, 0.8, -70)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(fx, fy, 2.0), rotation=(math.pi / 2, 0, math.radians(rz)))
    fo = bpy.context.object
    fo.scale = (2.0, 3.0, 1)
    assign(fo, flag)
    fo.visible_camera = False
    fo.visible_shadow = False
    fo.visible_diffuse = False
area('key', (-2.5, -3.0, 5.0), (0, 0, 2.0), 3.0, 260)
area('fill', (4.0, -3.0, 2.5), (0, 0, 2.0), 4.0, 140, (0.95, 0.97, 1.0))
area('back', (0.5, 5.0, 3.0), (0.5, 8, 1.5), 6.0, 650)
area('rim', (1.5, 3.0, 4.0), (0, 0, 2.0), 2.0, 300)
camera((0.0, -8.4, 2.4), (0.0, 0.0, 1.95), lens=50, dof=8.4, fstop=5.6)
render(out)
