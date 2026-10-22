"""Surgical Workflow AI: a laparoscopic grasper over a glass timeline of seven surgical phases.
Phase widths are illustrative (same as the existing card)."""
import bpy, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from mathutils import Vector, Euler

out, W, H, SPP, F = args()
reset(W, H, SPP, bg=(0.003, 0.004, 0.006))

root = bpy.data.objects.new('root', None)
bpy.context.collection.objects.link(root)
root.rotation_euler = (0, 0, F * 2 * math.pi)

# --- timeline bar ---
widths = [8, 22, 10, 26, 9, 15, 10]
cols = [(0.13, 0.55, 0.85), (0.20, 0.36, 0.92), (0.26, 0.20, 0.86), (0.48, 0.22, 0.82),
        (0.70, 0.18, 0.80), (0.82, 0.20, 0.66), (0.86, 0.22, 0.40)]
total = 3.4
gap = 0.035
scale = (total - gap * 6) / sum(widths)
x = -total / 2
shell = mat('shell', (0.95, 0.97, 1.0), rough=0.06, trans=1.0, ior=1.45, coat=0.4)
for i, (w, c) in enumerate(zip(widths, cols)):
    L = w * scale
    cx = x + L / 2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, 0, 0))
    o = bpy.context.object
    o.scale = (L, 0.26, 0.16)
    bpy.ops.object.transform_apply(scale=True)
    smooth(o, bevel=0.06, segments=8)
    assign(o, mat(f'sh{i}', tuple(0.55 + 0.45 * v for v in c), rough=0.05, trans=1.0, ior=1.45, coat=0.4))
    o.parent = root
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, 0, 0))
    core = bpy.context.object
    core.scale = (max(L - 0.07, 0.02), 0.17, 0.07)
    bpy.ops.object.transform_apply(scale=True)
    smooth(core, bevel=0.03, segments=6)
    assign(core, emission(f'c{i}', c, 1.4))
    core.parent = root
    x += L + gap

# playhead: inside phase 2
ph_x = -total / 2 + (8 + 7) * scale + gap
bpy.ops.mesh.primitive_cube_add(size=1, location=(ph_x, -0.16, 0.12))
ph = bpy.context.object
ph.scale = (0.018, 0.018, 0.62)
bpy.ops.object.transform_apply(scale=True)
smooth(ph, bevel=0.009, segments=4)
assign(ph, emission('ph', (1, 1, 1), 10))
ph.parent = root

# --- grasper ---
inst = bpy.data.objects.new('inst', None)
bpy.context.collection.objects.link(inst)
inst.parent = root
steel = mat('steel', (0.78, 0.78, 0.8), metal=1.0, rough=0.16)
black = mat('blackshaft', (0.012, 0.012, 0.014), rough=0.28, coat=0.7)
# shaft along +X from origin (tip at origin)
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.055, depth=6.0, location=(3.0 + 0.32, 0, 0), rotation=(0, math.pi / 2, 0))
sh = bpy.context.object
smooth(sh)
assign(sh, black)
sh.parent = inst
# metal collar
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.058, depth=0.2, location=(0.27, 0, 0), rotation=(0, math.pi / 2, 0))
co = bpy.context.object
smooth(co, bevel=0.01, segments=4)
assign(co, steel)
co.parent = inst
# hinge pin
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.022, depth=0.13, location=(0.17, 0, 0), rotation=(math.pi / 2, 0, 0))
pin = bpy.context.object
smooth(pin, bevel=0.005)
assign(pin, steel)
pin.parent = inst
# jaws: tapered, slightly open
for sgn in (1, -1):
    bpy.ops.mesh.primitive_cube_add(size=1)
    j = bpy.context.object
    j.scale = (0.46, 0.1, 0.055)
    bpy.ops.object.transform_apply(scale=True)
    for v in j.data.vertices:
        t = (0.23 - v.co.x) / 0.46  # 0 at hinge, 1 at tip
        v.co.y *= 1 - 0.45 * t
        v.co.z *= 1 - 0.35 * t
    j.location = (0, 0, 0)
    pivot = bpy.data.objects.new('pv', None)
    bpy.context.collection.objects.link(pivot)
    pivot.location = (0.17, 0, 0)
    pivot.parent = inst
    j.parent = pivot
    j.location = (-0.22, 0, sgn * 0.035)
    pivot.rotation_euler = (0, sgn * math.radians(-16), 0)
    smooth(j, bevel=0.012, segments=4)
    assign(j, steel)
# serrations on jaws (fine ridges)
inst.location = (ph_x - 0.02, -0.02, 0.42)
inst.rotation_euler = (math.radians(0), math.radians(-42), math.radians(-20))

# --- studio ---
floor = mat('floor', (0.003, 0.003, 0.004), rough=0.22, spec=0.3)
fl = backdrop(floor, size=40, z=-0.55)
key = area('key', (-1.0, -1.0, 4.5), (0, 0, 0), 1.6, 160, (0.95, 0.97, 1.0))
area('rim', (2.5, 3.5, 3.0), (0, 0, 0.3), 1.5, 260, (0.6, 0.55, 1.0))
area('strip', (-0.5, 3.0, 2.2), (0, 0, 0.4), 4.0, 90, (1, 1, 1), size_y=0.2)
for _l in ('key', 'rim', 'strip'):
    exclude(bpy.data.objects[_l], [fl])
camera((-3.3, -2.6, 1.55), (-0.25, 0.1, 0.05), lens=42, dof=3.9, fstop=4)
render(out)
