"""Muscle to Motion: the tendon-driven hand and forearm, re-modelled in simplified form from the
project's CAD (light-grey shell, dark panels, knurled wrist ring, jointed PLA fingers, palm plate).
Illustrative, not the CAD file itself."""
import bpy, math, sys, os, bmesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from mathutils import Vector, Matrix

out, W, H, SPP, F = args()
reset(W, H, SPP)

root = bpy.data.objects.new('root', None)
bpy.context.collection.objects.link(root)

shell = mat('shell', (0.36, 0.36, 0.365), rough=0.45, spec=0.45)
dark = mat('dark', (0.075, 0.075, 0.08), rough=0.5, spec=0.4)
pin = mat('pin', (0.3, 0.31, 0.33), metal=1.0, rough=0.4)
SY = 0.86  # oval cross-section


def rad(z):
    """Forearm radius: narrow at the cut end, fuller below the wrist."""
    t = z / 2.4
    return 0.29 + 0.07 * math.sin(min(1.0, t * 1.15) * math.pi / 2)


def link(o, m=None):
    if m:
        assign(o, m)
    o.parent = root
    return o


def surface(name, a0, a1, z0, z1, off, nu=48, nv=24):
    """A patch of the forearm surface between two angles and heights, pushed out by `off`."""
    me = bpy.data.meshes.new(name)
    verts, faces = [], []
    for j in range(nv + 1):
        z = z0 + (z1 - z0) * j / nv
        for i in range(nu + 1):
            a = a0 + (a1 - a0) * i / nu
            r = rad(z) + off
            verts.append((r * math.cos(a), r * SY * math.sin(a), z))
    for j in range(nv):
        for i in range(nu):
            k = j * (nu + 1) + i
            faces.append((k, k + 1, k + nu + 2, k + nu + 1))
    me.from_pydata(verts, [], faces)
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    return o


# forearm: closed lathe
prof = [(0.0, 0.0)] + [(rad(z), z) for z in [0.0, 0.03] + [i * 0.1 for i in range(1, 25)]] + [(0.3, 2.42), (0.0, 2.42)]
me = bpy.data.meshes.new('fore')
me.from_pydata([(r, 0, z) for r, z in prof], [(i, i + 1) for i in range(len(prof) - 1)], [])
fore = bpy.data.objects.new('fore', me)
bpy.context.collection.objects.link(fore)
sm = fore.modifiers.new('lathe', 'SCREW')
sm.angle = 2 * math.pi
sm.steps = sm.render_steps = 96
sm.use_merge_vertices = True
sm.use_normal_calculate = True
fore.scale = (1, SY, 1)
bv = fore.modifiers.new('bev', 'BEVEL'); bv.width = 0.02; bv.segments = 3; bv.limit_method = 'ANGLE'
smooth(fore)
link(fore, shell)

# dark inset panels on the front and side, as in the CAD
for nm, a0, a1, z0, z1 in (('p1', -2.2, -0.9, 1.0, 2.15), ('p2', -2.2, -0.9, 0.25, 0.85), ('p3', 0.9, 2.0, 1.2, 2.1)):
    p = surface(nm, a0, a1, z0, z1, 0.004)
    so = p.modifiers.new('sol', 'SOLIDIFY'); so.thickness = 0.018; so.offset = 1
    b = p.modifiers.new('bev', 'BEVEL'); b.width = 0.008; b.segments = 2; b.limit_method = 'ANGLE'
    smooth(p)
    link(p, dark)
    # two screw heads at the top corners
    for a in (a0 + 0.12, a1 - 0.12):
        z = z1 - 0.08
        r = rad(z) + 0.024
        n = Vector((math.cos(a), SY * math.sin(a), 0)).normalized()
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.022, depth=0.01, location=(r * math.cos(a), r * SY * math.sin(a), z))
        s = bpy.context.object
        s.rotation_euler = n.to_track_quat('Z', 'Y').to_euler()
        smooth(s)
        link(s, dark)

# wrist: neck, knurled ring, swivel
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.25, depth=0.12, location=(0, 0, 2.47))
link(smooth(bpy.context.object, bevel=0.02), shell)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.235, depth=0.26, location=(0, 0, 2.66))
link(smooth(bpy.context.object, bevel=0.02), dark)
for k in range(28):
    a = 2 * math.pi * k / 28
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.24 * math.cos(a), 0.24 * math.sin(a), 2.66))
    rb = bpy.context.object
    rb.scale = (0.035, 0.02, 0.2)
    rb.rotation_euler = (0, 0, a)
    link(smooth(rb, bevel=0.006, segments=2), dark)
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.17, depth=0.1, location=(0, 0, 2.83))
link(smooth(bpy.context.object, bevel=0.02), pin)

# palm: rounded block that tapers toward the wrist
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 3.27))
palm = bpy.context.object
palm.scale = (0.78, 0.3, 0.76)
bpy.ops.object.transform_apply(scale=True)
for v in palm.data.vertices:
    if v.co.z < 3.27:
        v.co.x *= 0.8
smooth(palm, bevel=0.1, segments=6)
link(palm, shell)
# palm plate on the front (palm) face
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.155, 3.25))
pl = bpy.context.object
pl.scale = (0.5, 0.03, 0.5)
bpy.ops.object.transform_apply(scale=True)
for v in pl.data.vertices:
    if v.co.z < 3.25:
        v.co.x *= 0.72
link(smooth(pl, bevel=0.02, segments=3), dark)
for x, z in ((-0.19, 3.44), (0.19, 3.44), (-0.13, 3.06), (0.13, 3.06)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.016, depth=0.01, location=(x, -0.172, z), rotation=(math.pi / 2, 0, 0))
    link(smooth(bpy.context.object), shell)


def finger(base, direction, lens, curl=4.0, w=0.1, d=0.13):
    """A chain of printed segments joined by pins, with a dark fingertip pad."""
    pos = Vector(base)
    dirv = Vector(direction).normalized()
    side = Vector((1, 0, 0)) if abs(dirv.x) < 0.7 else Vector((0, 1, 0))
    for n, L in enumerate(lens):
        q = dirv.to_track_quat('Z', 'Y')
        mid = pos + dirv * (L / 2)
        bpy.ops.mesh.primitive_cube_add(size=1, location=mid)
        sgm = bpy.context.object
        sgm.scale = (w, d, L - 0.04)
        sgm.rotation_euler = q.to_euler()
        link(smooth(sgm, bevel=0.04, segments=5), shell)
        # joint pin
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.03, depth=w + 0.03, location=pos)
        pn = bpy.context.object
        pn.rotation_euler = (q @ Quaternion_axis_y()).to_euler()
        link(smooth(pn), pin)
        pos = pos + dirv * L
        # curl slightly toward the palm side (-y)
        dirv = (Matrix.Rotation(math.radians(curl), 3, q @ Vector((1, 0, 0))) @ dirv).normalized()
    # dark fingertip cap over the last segment's end
    q = dirv.to_track_quat('Z', 'Y')
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos - dirv * 0.07)
    tp = bpy.context.object
    tp.scale = (w + 0.012, d + 0.012, 0.13)
    tp.rotation_euler = q.to_euler()
    link(smooth(tp, bevel=0.035, segments=4), dark)


def Quaternion_axis_y():
    from mathutils import Quaternion
    return Quaternion((0, 1, 0), math.pi / 2)


for x, L in ((-0.285, (0.4, 0.32, 0.27)), (-0.095, (0.45, 0.36, 0.29)), (0.095, (0.44, 0.35, 0.29)), (0.285, (0.38, 0.3, 0.25))):
    finger((x, 0, 3.67), (x * 0.12, 0, 1), L)
# thumb out to the side
finger((0.42, -0.03, 3.05), (0.8, -0.15, 0.55), (0.32, 0.27), curl=6)

root.rotation_euler = (0, 0, math.radians(28) + F * 2 * math.pi)

studio(z=0.0)
area('key', (-3.0, -4.0, 6.5), (0, 0, 2.8), 3.5, 160)
area('fill', (4.5, -3.0, 3.0), (0, 0, 2.6), 4.0, 60, (0.95, 0.97, 1.0))
area('rim', (1.0, 4.0, 5.0), (0, 0, 3.0), 2.5, 300)
camera((0.0, -10.5, 6.4), (0.0, 0.0, 3.2), lens=74, dof=11.0, fstop=5.6)
render(out)
