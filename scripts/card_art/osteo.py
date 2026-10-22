"""OsteoTrack: a clear-glass lower leg with a tibia inside it, broken mid-shaft with a jagged,
slightly displaced fracture. A soft cuff with the vibration module sits on the leg beside the break,
and two sensor strips sit above and below it. Illustrates the proposed concept, not a built device."""
import bpy, math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from mathutils import Vector

out, W, H, SPP, F = args()
sc = reset(W, H, SPP)
random.seed(4)

root = bpy.data.objects.new('root', None)
bpy.context.collection.objects.link(root)


def lathe(name, prof, steps=96, sx=1.0, sy=1.0):
    me = bpy.data.meshes.new(name)
    me.from_pydata([(r, 0, z) for r, z in prof], [(i, i + 1) for i in range(len(prof) - 1)], [])
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    sm = o.modifiers.new('lathe', 'SCREW')
    sm.angle = 2 * math.pi
    sm.steps = sm.render_steps = steps
    sm.use_merge_vertices = True
    sm.use_normal_calculate = True
    sub = o.modifiers.new('sub', 'SUBSURF')
    sub.levels = sub.render_levels = 2
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier='lathe')
    bpy.ops.object.modifier_apply(modifier='sub')
    o.scale = (sx, sy, 1)
    bpy.ops.object.transform_apply(scale=True)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


# tibia-like profile: wide plateau on top, narrow mid-shaft, smaller ankle end
tib = [(0.0, -2.0), (0.2, -1.99), (0.27, -1.92), (0.26, -1.78), (0.19, -1.5), (0.15, -1.0), (0.145, -0.3),
       (0.15, 0.3), (0.17, 0.9), (0.24, 1.35), (0.36, 1.66), (0.42, 1.8), (0.41, 1.9), (0.3, 1.96), (0.0, 1.97)]
bone = lathe('tibia', tib, sx=1.0, sy=0.82)
bone_m = mat('bone', (0.7, 0.63, 0.5), rough=0.6, coat=0.05)
_nt = bone_m.node_tree
_n = _nt.nodes.new('ShaderNodeTexNoise'); _n.inputs['Scale'].default_value = 60; _n.inputs['Detail'].default_value = 8
_mp = _nt.nodes.new('ShaderNodeMapping'); _mp.inputs['Scale'].default_value = (1, 1, 0.12)
_tc = _nt.nodes.new('ShaderNodeTexCoord')
_nt.links.new(_tc.outputs['Object'], _mp.inputs[0]); _nt.links.new(_mp.outputs[0], _n.inputs['Vector'])
_b = _nt.nodes.new('ShaderNodeBump'); _b.inputs['Strength'].default_value = 0.25
_nt.links.new(_n.outputs['Fac'], _b.inputs['Height']); _nt.links.new(_b.outputs[0], _nt.nodes['Principled BSDF'].inputs['Normal'])
bone_m.node_tree.nodes['Principled BSDF'].inputs['Subsurface Weight'].default_value = 0.25
bone_m.node_tree.nodes['Principled BSDF'].inputs['Subsurface Radius'].default_value = (0.08, 0.05, 0.03)
assign(bone, bone_m)
marrow = mat('marrow', (0.5, 0.36, 0.24), rough=0.95)

# fracture: split the bone on a tilted plane, cap each side, then roughen both caps with the
# same noise so the two fragments still match like a real break
import bmesh
PN = Vector((-0.24, 0.0, 1.0)).normalized()


def jag(co):
    x, y = co.x, co.y
    return 0.07 * math.sin(x * 33 + 1.3) * math.cos(y * 29) + 0.03 * math.sin(x * 97) * math.sin(y * 83 + 0.7)


def half(src, keep_top):
    o = src.copy()
    o.data = src.data.copy()
    bpy.context.collection.objects.link(o)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    r = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0), plane_no=PN, clear_outer=keep_top is False, clear_inner=keep_top is True)
    edges = [e for e in r['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
    f = bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=False, edges=edges)
    caps = [g for g in f['geom'] if isinstance(g, bmesh.types.BMFace)]
    sub = bmesh.ops.subdivide_edges(bm, edges=list({e for fc in caps for e in fc.edges}), cuts=5, use_grid_fill=True)
    for v in bm.verts:
        d = v.co.dot(PN)
        if abs(d) < 1e-4:
            v.co += PN * jag(v.co)
    bm.normal_update()
    bm.to_mesh(o.data)
    bm.free()
    o.data.materials.append(bone_m)
    o.data.materials.append(marrow)
    for p in o.data.polygons:
        cap = abs(p.center.dot(PN)) < 0.09 and Vector((p.center.x, p.center.y, 0)).length < 0.15
        p.material_index = 1 if cap else 0
        p.use_smooth = not cap
    return o


top = half(bone, True)
low = half(bone, False)
bpy.data.objects.remove(bone)
bone = low
# displace the upper fragment a little: a real, slightly angulated break
top.location = (0.09, -0.02, 0.2)
top.rotation_euler = (math.radians(3), math.radians(-7), 0)
for o in (bone, top):
    o.parent = root

# cuff on the leg just below the break, with the vibration module and contact disc
z_c = -0.75
r_leg = 0.19
bpy.ops.mesh.primitive_torus_add(major_radius=r_leg + 0.02, minor_radius=0.06, major_segments=128, minor_segments=32, location=(0, 0, z_c))
cuff = bpy.context.object
cuff.scale = (1, 0.85, 2.6)
smooth(cuff)
assign(cuff, mat('cuff', (0.06, 0.16, 0.45), rough=0.45, sheen=0.4))
cuff.parent = root
alu = mat('alu', (0.72, 0.73, 0.76), metal=1.0, rough=0.25)
slate = mat('slate', (0.05, 0.055, 0.065), rough=0.3, coat=0.8)
y_f = -(r_leg * 0.85 + 0.1)
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.17, depth=0.1, location=(0, y_f, z_c), rotation=(math.pi / 2, 0, 0))
mod = bpy.context.object
smooth(mod, bevel=0.025, segments=6)
assign(mod, alu)
mod.parent = root
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.13, depth=0.02, location=(0, y_f - 0.055, z_c), rotation=(math.pi / 2, 0, 0))
face = bpy.context.object
smooth(face, bevel=0.005, segments=3)
assign(face, slate)
face.parent = root

# two accelerometer strips, above and below the break
strip = mat('strip', (0.1, 0.11, 0.13), rough=0.5)
for z in (0.75, -1.55):
    rr = 0.2 if z > 0 else 0.17
    bpy.ops.mesh.primitive_torus_add(major_radius=rr + 0.01, minor_radius=0.014, major_segments=128, minor_segments=12, location=(0, 0, z))
    s = bpy.context.object
    s.scale = (1, 0.84, 2.0)
    smooth(s)
    assign(s, strip)
    s.parent = root
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -(rr * 0.84 + 0.045), z))
    pod = bpy.context.object
    pod.scale = (0.13, 0.05, 0.09)
    bpy.ops.object.transform_apply(scale=True)
    smooth(pod, bevel=0.02, segments=5)
    assign(pod, slate)
    pod.parent = root

root.location = (0, 0, 2.6)
root.rotation_euler = (0, math.radians(-24), math.radians(25) + F * 2 * math.pi)

fl = studio(z=0.0)
flag = mat('flag', (0, 0, 0), rough=0.6, spec=0.0)
for fx, fy, rz in ((-3.2, 0.5, 70), (3.2, 0.8, -70)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(fx, fy, 2.6), rotation=(math.pi / 2, 0, math.radians(rz)))
    fo = bpy.context.object
    fo.scale = (2.0, 4.0, 1)
    assign(fo, flag)
    fo.visible_camera = False
    fo.visible_shadow = False
    fo.visible_diffuse = False
area('key', (-2.5, -3.0, 6.0), (0, 0, 2.6), 3.0, 220)
area('fill', (4.0, -3.0, 3.0), (0, 0, 2.6), 4.0, 140, (0.95, 0.97, 1.0))
area('rim', (1.5, 3.0, 5.0), (0, 0, 2.6), 2.0, 360)
camera((0.0, -9.6, 2.9), (0.0, 0.0, 2.55), lens=95, dof=9.6, fstop=4)
render(out)
