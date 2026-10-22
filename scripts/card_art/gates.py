"""Gate-Level Heart Monitor: sculpted logic gates (XOR, AND, OR) feeding a green / amber / red alarm.
Symbolic, not a picture of hardware: the project was designed and tested in simulation."""
import bpy, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from mathutils import Vector

out, W, H, SPP, F = args()
reset(W, H, SPP, bg=(0.002, 0.003, 0.004))

root = bpy.data.objects.new('root', None)
bpy.context.collection.objects.link(root)
root.rotation_euler = (0, 0, math.radians(-72) + F * 2 * math.pi)
root.location = (0.05, 0.25, 0)


def arc(cx, cy, r, a0, a1, n=40):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def bez(p0, p1, p2, n=40):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]


def and_shape():
    return [(0, 0), (0.55, 0)] + arc(0.55, 0.5, 0.5, -math.pi / 2, math.pi / 2)[1:-1] + [(0.55, 1), (0, 1)]


def or_shape(back=0.0):
    pts = bez((back, 0), (0.75 + back, 0.0), (1.15 + back, 0.5))[:-1]
    pts += bez((1.15 + back, 0.5), (0.75 + back, 1.0), (back, 1))[:-1]
    pts += bez((back, 1), (0.28 + back, 0.5), (back, 0))[:-1]
    return pts


def solid(name, pts, depth, m, loc, rot_z=0):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '2D'
    cu.fill_mode = 'BOTH'
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for i, (x, y) in enumerate(pts):
        sp.points[i].co = (x - 0.55, y - 0.5, 0, 1)
    sp.use_cyclic_u = True
    cu.extrude = depth
    cu.bevel_depth = 0.035
    cu.bevel_resolution = 6
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    o.location = loc
    o.rotation_euler = (0, 0, rot_z)
    o.parent = root
    return o


def tube(name, pts, r, m):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        sp.points[i].co = (*p, 1)
    cu.bevel_depth = r
    cu.bevel_resolution = 4
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    o.parent = root
    return o


ceramic = mat('ceramic', (0.02, 0.022, 0.026), rough=0.22, coat=1.0, spec=0.5)
glass = mat('glass', (0.9, 0.95, 1.0), rough=0.03, trans=1.0, ior=1.5)
edge = emission('edge', (0.35, 0.6, 1.0), 6)

z = 0.18
gates = [
    ('xor', or_shape(0.12), (-1.4, 0.7, z)),
    ('and', and_shape(), (-1.4, -0.7, z)),
    ('or', or_shape(0.0), (0.6, 0.0, z)),
]
for name, pts, loc in gates:
    solid(name, pts, 0.16, ceramic, loc)
    o = solid(name + '_inlay', [(x, y) for x, y in pts], 0.0, edge, (loc[0], loc[1], loc[2] + 0.2))
    o.scale = (0.86, 0.82, 1)
    o.data.fill_mode = 'NONE'
    o.data.bevel_depth = 0.008
    if name == 'xor':
        back = [(x - 0.55, y - 0.5) for x, y in bez((0, 0), (0.28, 0.5), (0, 1))]
        tube('xor_back', [(loc[0] + x, loc[1] + y, loc[2] + 0.08) for x, y in back], 0.03, ceramic)

wire = emission('wire', (0.35, 0.6, 1.0), 4)
wz = 0.1
for gy, bx in ((0.7, -1.78), (-0.7, -1.95)):
    for dy in (-0.25, 0.25):
        tube(f'in{gy}{dy}', [(-5.0, gy + dy, wz), (bx, gy + dy, wz)], 0.014, wire)
tube('x2or', [(-0.68, 0.7, wz), (-0.25, 0.7, wz), (-0.25, 0.25, wz), (0.12, 0.25, wz)], 0.014, wire)
tube('a2or', [(-0.9, -0.7, wz), (-0.25, -0.7, wz), (-0.25, -0.25, wz), (0.12, -0.25, wz)], 0.014, wire)
tube('or2bus', [(1.2, 0.0, wz), (1.65, 0.0, wz)], 0.014, wire)
tube('bus', [(1.65, 0.75, wz), (1.65, -0.75, wz)], 0.014, wire)
for yy in (0.75, -0.75):
    tube(f'tap{yy}', [(1.65, yy, wz), (1.95, yy, wz)], 0.014, wire)
tube('tap0', [(1.65, 0.0, wz), (1.95, 0.0, wz)], 0.014, wire)

# alarm: three glass domes, green / amber / red
cols = [(0.12, 1.0, 0.3), (1.0, 0.5, 0.04), (1.0, 0.06, 0.05)]
for i, c in enumerate(cols):
    x, y = 2.3, -0.75 + i * 0.75
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.3, depth=0.12, location=(x, y, 0.06))
    b = bpy.context.object
    smooth(b, bevel=0.02, segments=4)
    assign(b, ceramic)
    b.parent = root
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=0.24, location=(x, y, 0.12))
    d = bpy.context.object
    d.scale = (1, 1, 0.85)
    smooth(d)
    assign(d, glass)
    d.parent = root
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.11, location=(x, y, 0.14))
    core = bpy.context.object
    smooth(core)
    assign(core, emission(f'core{i}', c, 7))
    core.parent = root
    l = bpy.data.lights.new(f'l{i}', 'POINT')
    l.energy = 12
    l.color = c
    l.shadow_soft_size = 0.1
    lo = bpy.data.objects.new(f'l{i}', l)
    bpy.context.collection.objects.link(lo)
    lo.location = (x, y, 0.15)
    lo.parent = root

fl = studio(z=0.0)
k = area('key', (-2.5, -3.0, 5.0), (0, 0, 0), 3.0, 380, (0.9, 0.93, 1.0))
r = area('rim', (3.0, 4.0, 2.5), (0, 0.5, 0), 3.0, 600, (0.55, 0.7, 1.0))
s = area('strip', (-4.0, 2.0, 2.0), (0, 0, 0), 4.0, 220, (1, 1, 1), size_y=0.3)
for l in (k, r, s):
    exclude(l, [fl])
camera((0.0, -8.0, 6.2), (0.0, -0.1, 0.0), lens=46, dof=10.1, fstop=5.6)
render(out)
