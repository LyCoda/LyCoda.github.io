"""Implant Follow-up: a generic titanium fixation plate with a porous lattice zone and two screws,
on a white studio sweep. Illustrative only; not a KOLN 3D product."""
import bpy, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from mathutils import Vector

out, W, H, SPP, F = args()
sc = reset(W, H, SPP, bg=(0.93, 0.94, 0.95), strength=0.45)

root = bpy.data.objects.new('root', None)
bpy.context.collection.objects.link(root)
root.rotation_euler = (0, 0, math.radians(-62) + F * 2 * math.pi)

ti = mat('ti', (0.62, 0.59, 0.55), metal=1.0, rough=0.36)
ti_dark = mat('tid', (0.42, 0.41, 0.4), metal=1.0, rough=0.28)

# plate outline: a stadium with lobes around each screw hole
holes = [(-1.3, 0), (-0.65, 0), (0.65, 0), (1.3, 0)]
bpy.ops.mesh.primitive_cube_add(size=1)
plate = bpy.context.object
plate.scale = (2.6, 0.42, 0.07)
bpy.ops.object.transform_apply(scale=True)
for hx, hy in holes:
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.26, depth=0.07, location=(hx, hy, 0))
    lobe = bpy.context.object
    m = plate.modifiers.new('u', 'BOOLEAN')
    m.operation = 'UNION'
    m.object = lobe
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier='u')
    bpy.data.objects.remove(lobe)
# lattice window in the middle: a grid of small square holes
bpy.ops.mesh.primitive_cube_add(size=1)
grid = bpy.context.object
grid.scale = (0.055, 0.055, 0.3)
bpy.ops.object.transform_apply(scale=True)
arr = grid.modifiers.new('ax', 'ARRAY')
arr.count = 8
arr.relative_offset_displace = (1.75, 0, 0)
arr2 = grid.modifiers.new('ay', 'ARRAY')
arr2.count = 4
arr2.relative_offset_displace = (0, 1.75, 0)
grid.location = (-0.34, -0.145, 0)
bpy.context.view_layer.objects.active = grid
bpy.ops.object.modifier_apply(modifier='ax')
bpy.ops.object.modifier_apply(modifier='ay')
m = plate.modifiers.new('d', 'BOOLEAN')
m.operation = 'DIFFERENCE'
m.object = grid
bpy.context.view_layer.objects.active = plate
bpy.ops.object.modifier_apply(modifier='d')
bpy.data.objects.remove(grid)
# countersunk screw holes
for hx, hy in holes:
    bpy.ops.mesh.primitive_cone_add(vertices=96, radius1=0.08, radius2=0.16, depth=0.08, location=(hx, hy, 0.0))
    c = bpy.context.object
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.08, depth=0.3, location=(hx, hy, 0))
    c2 = bpy.context.object
    for cut in (c, c2):
        m = plate.modifiers.new('h', 'BOOLEAN')
        m.operation = 'DIFFERENCE'
        m.object = cut
        bpy.context.view_layer.objects.active = plate
        bpy.ops.object.modifier_apply(modifier='h')
        bpy.data.objects.remove(cut)
smooth(plate, bevel=0.012, segments=3)
bpy.context.view_layer.objects.active = plate
bpy.ops.object.modifier_apply(modifier='bev')
# bend it gently, as if contoured to bone
plate.location = (0, 0, 0)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.subdivide(number_cuts=2)
bpy.ops.object.mode_set(mode='OBJECT')
for v in plate.data.vertices:
    v.co.z += -0.16 * (v.co.x / 1.5) ** 2 + 0.04 * math.sin(v.co.x * 1.7)
for p in plate.data.polygons:
    p.use_smooth = True
plate.data.shade_auto_smooth(angle=math.radians(35)) if hasattr(plate.data, 'shade_auto_smooth') else None
assign(plate, ti)
plate.parent = root
plate.location = (0, 0, 0.55)
plate.rotation_euler = (math.radians(14), math.radians(-8), 0)


def screw(loc, rot, length=0.9):
    s = bpy.data.objects.new('screw', None)
    bpy.context.collection.objects.link(s)
    s.parent = root
    s.location = loc
    s.rotation_euler = rot
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.13, depth=0.08, location=(0, 0, 0))
    head = bpy.context.object
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.055, depth=0.1, location=(0, 0, 0.04))
    hexo = bpy.context.object
    m = head.modifiers.new('hx', 'BOOLEAN')
    m.operation = 'DIFFERENCE'
    m.object = hexo
    bpy.context.view_layer.objects.active = head
    bpy.ops.object.modifier_apply(modifier='hx')
    bpy.data.objects.remove(hexo)
    smooth(head, bevel=0.012, segments=3)
    assign(head, ti_dark)
    head.parent = s
    # threaded shank: a helix of small torus-like ridges via screw modifier on a profile
    verts = [(0.05, 0, 0), (0.075, 0, 0.02), (0.05, 0, 0.04)]
    me = bpy.data.meshes.new('prof')
    me.from_pydata(verts, [(0, 1), (1, 2)], [])
    th = bpy.data.objects.new('thread', me)
    bpy.context.collection.objects.link(th)
    sm = th.modifiers.new('sc', 'SCREW')
    sm.screw_offset = 0.04
    sm.iterations = int(length / 0.04)
    sm.steps = 48
    sm.render_steps = 48
    th.location = (0, 0, -length - 0.04)
    for p in th.data.polygons:
        p.use_smooth = True
    th.data.materials.append(ti_dark)
    th.parent = s
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.052, depth=length, location=(0, 0, -length / 2 - 0.04))
    core = bpy.context.object
    smooth(core)
    assign(core, ti_dark)
    core.parent = s
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.052, radius2=0.0, depth=0.1, location=(0, 0, -length - 0.09), rotation=(math.pi, 0, 0))
    tip = bpy.context.object
    tip.rotation_euler = (math.pi, 0, 0)
    smooth(tip)
    assign(tip, ti_dark)
    tip.parent = s


screw((-0.25, -0.95, 0.13), (math.radians(90), 0, math.radians(-25)), 0.75)
screw((0.45, -1.15, 0.13), (math.radians(90), 0, math.radians(-160)), 0.6)

flag = mat('flag', (0.0, 0.0, 0.0), rough=0.6, spec=0.0)
for fx, fy, rz in ((-3.2, 0.5, 70), (3.2, 0.8, -70), (0.0, 3.0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(fx, fy, 1.2), rotation=(math.pi / 2, 0, math.radians(rz)))
    fo = bpy.context.object
    fo.scale = (2.4, 2.0, 1)
    assign(fo, flag)
    fo.visible_camera = False
    fo.visible_shadow = False
    fo.visible_diffuse = False
floor = mat('floor', (0.9, 0.9, 0.92), rough=0.55, spec=0.3)
backdrop(floor, size=40, z=0.0)
area('key', (-2.0, -2.5, 5.0), (0, 0, 0.4), 3.0, 520)
area('fill', (4.0, -3.0, 2.0), (0, 0, 0.4), 4.0, 160, (0.95, 0.97, 1.0))
area('back', (0.5, 5.0, 3.0), (0.5, 8, 1.5), 6.0, 900)
area('strip', (3.0, 1.0, 2.0), (0, 0, 0.5), 4.0, 260, (1, 1, 1), size_y=0.3)
camera((0.2, -6.2, 4.6), (-0.25, -0.3, 0.3), lens=58, dof=7.5, fstop=5.6)
render(out)
