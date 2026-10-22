"""Walking & the Brain: a frosted-glass head with an fNIRS-style headband.
Light paths between source and detector pods are illustrative, not study data."""
import bpy, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from mathutils import Vector

out, W, H, SPP, F = args()
reset(W, H, SPP, bg=(0.004, 0.004, 0.007))
spin = F * 2 * math.pi

root = bpy.data.objects.new('root', None)
bpy.context.collection.objects.link(root)
root.rotation_euler = (math.radians(-14), 0, spin)
root.location = (0, 0, -0.35)

# Glass head volume
bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=64, radius=1)
head = bpy.context.object
head.scale = (0.9, 1.08, 1.25)
head.location = (0, 0, 0)
smooth(head)
glass = mat('glass', (0.32, 0.36, 0.44), rough=0.12, trans=1.0, ior=1.2, coat=0.6)
assign(head, glass)
head.parent = root

# Headband
z = 0.38
k = math.sqrt(1 - (z / 1.25) ** 2)
bpy.ops.curve.primitive_bezier_circle_add(radius=1)
band = bpy.context.object
band.scale = (0.9 * k + 0.035, 1.08 * k + 0.035, 1)
band.location = (0, 0, z)
band.data.extrude = 0.075
band.data.bevel_depth = 0.022
band.data.bevel_resolution = 6
band.data.resolution_u = 64
band.data.fill_mode = 'FULL'
bpy.ops.object.convert(target='MESH')
band = bpy.context.object
smooth(band)
soft = mat('soft', (0.018, 0.018, 0.02), rough=0.62, sheen=0.4, spec=0.4)
assign(band, soft)
band.parent = root

red = emission('red', (1.0, 0.08, 0.06), 30)
red_soft = emission('redsoft', (1.0, 0.12, 0.08), 22)
blue_soft = emission('bluesoft', (0.15, 0.35, 1.0), 22)
alu = mat('alu', (0.62, 0.63, 0.66), metal=1.0, rough=0.28)
lens = mat('lens', (0.01, 0.015, 0.03), rough=0.05, coat=1.0)
ring_blue = emission('ringblue', (0.2, 0.45, 1.0), 12)


def on_band(a, r_off=0.0):
    rx, ry = 0.9 * k + 0.035 + r_off, 1.08 * k + 0.035 + r_off
    p = Vector((rx * math.sin(a), -ry * math.cos(a), z))
    # outward normal of the ellipse
    n = Vector((math.sin(a) / rx, -math.cos(a) / ry, 0)).normalized()
    return p, n


pods = []
angles = [math.radians(d) for d in (-66, -44, -22, 0, 22, 44, 66)]
for i, a in enumerate(angles):
    p, n = on_band(a, 0.022)
    src = i % 2 == 0
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.085, depth=0.05)
    pod = bpy.context.object
    pod.location = p + n * 0.025
    pod.rotation_euler = n.to_track_quat('Z', 'Y').to_euler()
    smooth(pod, bevel=0.012, segments=5)
    assign(pod, alu)
    pod.parent = root
    # face: lens or emitter
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.05, depth=0.012)
    face = bpy.context.object
    face.location = p + n * 0.052
    face.rotation_euler = pod.rotation_euler
    smooth(face, bevel=0.004, segments=3)
    assign(face, red if src else lens)
    face.parent = root
    if not src:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.064, minor_radius=0.0045, major_segments=96, minor_segments=12)
        t = bpy.context.object
        t.location = p + n * 0.052
        t.rotation_euler = pod.rotation_euler
        assign(t, ring_blue)
        t.parent = root
    pods.append((p, n, src))

# Banana-shaped light paths from each source into the head and back to the neighbouring detector
for i in range(len(pods) - 1):
    (p0, n0, s0), (p1, n1, s1) = pods[i], pods[i + 1]
    mid = (p0 + p1) / 2
    inward = -((n0 + n1) / 2).normalized()
    depth = 0.34
    pts = []
    for j in range(25):
        t = j / 24
        base = p0.lerp(p1, t)
        d = math.sin(math.pi * t) * depth
        pts.append(base + inward * d * 0.75 + Vector((0, 0, -math.sin(math.pi * t) * 0.3)))
    cu = bpy.data.curves.new(f'path{i}', 'CURVE')
    cu.dimensions = '3D'
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for j, q in enumerate(pts):
        sp.points[j].co = (*q, 1)
    cu.bevel_depth = 0.008
    cu.bevel_resolution = 4
    o = bpy.data.objects.new(f'path{i}', cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(red_soft if i % 2 == 0 else blue_soft)
    o.parent = root
    # a softer halo around the path
    cu2 = cu.copy()
    cu2.bevel_depth = 0.03
    o2 = bpy.data.objects.new(f'halo{i}', cu2)
    bpy.context.collection.objects.link(o2)
    halo = mat(f'halo{i}', (0, 0, 0), rough=1, emit=(1.0, 0.15, 0.1) if i % 2 == 0 else (0.2, 0.4, 1.0), emit_strength=0.35, alpha=0.18)
    o2.data.materials.clear()
    o2.data.materials.append(halo)
    o2.parent = root

# Dark studio
floor = mat('floor', (0.004, 0.004, 0.006), rough=0.3, spec=0.4)
fl = backdrop(floor, size=40, z=-0.75)
area('key', (-2.6, -2.2, 4.6), (0, 0, 0.0), 5.0, 300, (0.92, 0.95, 1.0))
area('rim', (3.4, 2.6, 1.6), (0, 0, 0.3), 2.2, 700, (0.55, 0.65, 1.0))
area('rim2', (-2.5, 3.5, 3.5), (0, 0, 0.0), 3.5, 300, (1.0, 0.45, 0.45))
area('top', (0, 0, 5), (0, 0, 0), 4.0, 120)
for _l in ('key', 'rim', 'rim2', 'top'):
    exclude(bpy.data.objects[_l], [fl])
camera((1.0, -4.4, 1.25), (0.0, -0.4, -0.05), lens=55, dof=3.55, fstop=2.8)
render(out)
