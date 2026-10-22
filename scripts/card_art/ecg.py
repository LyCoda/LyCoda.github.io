"""ECG Amplifier: a breadboard with an 8-pin instrumentation-amp chip, a few passives,
and a glowing heartbeat trace floating above it. Illustrative, not the real build."""
import bpy, math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from mathutils import Vector

out, W, H, SPP, F = args()
reset(W, H, SPP, bg=(0.002, 0.003, 0.004))
random.seed(5)

root = bpy.data.objects.new('root', None)
bpy.context.collection.objects.link(root)
root.rotation_euler = (0, 0, math.radians(-22) + F * 2 * math.pi)

# hole-grid texture for the breadboard, drawn with PIL-free pure Python into a Blender image
TW, TH = 1024, 640
img = bpy.data.images.new('holes', TW, TH)
px = [1.0] * (TW * TH * 4)
pitch = 16
for y in range(TH):
    for x in range(TW):
        gx, gy = x % pitch, y % pitch
        row = y // pitch
        hole = 4 <= gx <= 11 and 4 <= gy <= 11
        gutter = 18 <= row <= 20  # centre channel
        rail = row in (2, 3, 36, 37)
        dark = hole and not gutter and (row not in (0, 1, 4, 5, 34, 35, 38, 39))
        i = (y * TW + x) * 4
        v = 0.04 if dark else 1.0
        if gutter and 18 < row < 20:
            v = 0.6
        px[i:i + 3] = [v, v, v]
        if rail and gy == 1:
            c = (0.9, 0.15, 0.12) if row in (2, 36) else (0.1, 0.3, 0.9)
            px[i:i + 3] = list(c)
img.pixels = px

bb = bpy.data.materials.new('bb')
bb.use_nodes = True
nt = bb.node_tree
p = nt.nodes['Principled BSDF']
tex = nt.nodes.new('ShaderNodeTexImage')
tex.image = img
tex.interpolation = 'Closest'
mix = nt.nodes.new('ShaderNodeMixRGB')
mix.blend_type = 'MULTIPLY'
mix.inputs[0].default_value = 1
mix.inputs[1].default_value = (0.93, 0.93, 0.9, 1)
nt.links.new(tex.outputs[0], mix.inputs[2])
nt.links.new(mix.outputs[0], p.inputs['Base Color'])
p.inputs['Roughness'].default_value = 0.42
bump = nt.nodes.new('ShaderNodeBump')
bump.inputs['Strength'].default_value = 0.6
nt.links.new(tex.outputs[0], bump.inputs['Height'])
nt.links.new(bump.outputs[0], p.inputs['Normal'])

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.09))
board = bpy.context.object
board.scale = (3.2, 2.0, 0.18)
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.material_slot_add()
board.data.materials[0] = bb
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.cube_project(cube_size=1.0)
bpy.ops.object.mode_set(mode='OBJECT')
# top face UV = full texture
me = board.data
uv = me.uv_layers.active.data
for poly in me.polygons:
    if poly.normal.z > 0.9:
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            uv[li].uv = ((v.x + 1.6) / 3.2, (v.y + 1.0) / 2.0)
smooth(board, bevel=0.02, segments=3)
board.parent = root

epoxy = mat('epoxy', (0.015, 0.015, 0.017), rough=0.45)
tin = mat('tin', (0.82, 0.82, 0.84), metal=1.0, rough=0.22)
bodyb = mat('resb', (0.55, 0.72, 0.9), rough=0.35, coat=0.6)
ceram = mat('cer', (0.85, 0.6, 0.15), rough=0.3, coat=0.5)


def box(loc, size, m, bevel=0.01):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    smooth(o, bevel=bevel, segments=3)
    assign(o, m)
    o.parent = root
    return o


# 8-pin DIP chip straddling the centre channel
box((0.0, 0.0, 0.25), (0.42, 0.3, 0.12), epoxy, 0.012)
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.025, depth=0.004, location=(-0.15, -0.08, 0.312))
d = bpy.context.object
assign(d, mat('dot', (0.04, 0.04, 0.04), rough=0.2))
d.parent = root
for k in range(4):
    for s in (-1, 1):
        box((-0.15 + k * 0.1, s * 0.17, 0.2), (0.03, 0.06, 0.1), tin, 0.004)


# resistors: body with bands and bent leads
def resistor(x, y, rot, bands):
    grp = bpy.data.objects.new('r', None)
    bpy.context.collection.objects.link(grp)
    grp.parent = root
    grp.location = (x, y, 0.3)
    grp.rotation_euler = (0, 0, rot)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.045, depth=0.24, rotation=(0, math.pi / 2, 0))
    b = bpy.context.object
    smooth(b, bevel=0.02, segments=4)
    assign(b, bodyb)
    b.parent = grp
    for j, c in enumerate(bands):
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.047, depth=0.022, location=(-0.07 + j * 0.045, 0, 0), rotation=(0, math.pi / 2, 0))
        bd = bpy.context.object
        smooth(bd)
        assign(bd, mat(f'band{j}{c}', c, rough=0.4))
        bd.parent = grp
    for s in (-1, 1):
        pts = [(s * 0.12, 0, 0), (s * 0.24, 0, 0), (s * 0.26, 0, -0.03), (s * 0.26, 0, -0.14)]
        cu = bpy.data.curves.new('lead', 'CURVE')
        cu.dimensions = '3D'
        sp = cu.splines.new('POLY')
        sp.points.add(len(pts) - 1)
        for i, q in enumerate(pts):
            sp.points[i].co = (*q, 1)
        cu.bevel_depth = 0.008
        o = bpy.data.objects.new('lead', cu)
        bpy.context.collection.objects.link(o)
        o.data.materials.append(tin)
        o.parent = grp


brown, black, red, gold, orange, yellow = (0.25, 0.1, 0.03), (0.02, 0.02, 0.02), (0.7, 0.05, 0.03), (0.75, 0.55, 0.2), (0.9, 0.35, 0.03), (0.9, 0.75, 0.05)
resistor(-0.9, 0.55, 0, [brown, black, orange, gold])
resistor(-0.9, -0.55, 0, [yellow, red, red, gold])
resistor(0.85, 0.5, math.pi / 2, [red, red, orange, gold])
# ceramic capacitors (blobs on two legs)
for (x, y) in ((0.75, -0.6), (1.05, -0.6)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.06, location=(x, y, 0.38))
    c = bpy.context.object
    c.scale = (1, 0.45, 1)
    smooth(c)
    assign(c, ceram)
    c.parent = root
    for s in (-1, 1):
        box((x + s * 0.025, y, 0.27), (0.012, 0.012, 0.16), tin, 0.002)

# jumper wires
for (pts, col) in ((([-1.3, 0.85, 0.2], [-1.3, 0.85, 0.42], [-0.5, 0.85, 0.42], [-0.5, 0.85, 0.2]), (0.85, 0.12, 0.1)),
                   (([0.3, -0.85, 0.2], [0.3, -0.85, 0.36], [1.3, -0.85, 0.36], [1.3, -0.85, 0.2]), (0.1, 0.35, 0.9))):
    cu = bpy.data.curves.new('wire', 'CURVE')
    cu.dimensions = '3D'
    sp = cu.splines.new('BEZIER')
    sp.bezier_points.add(len(pts) - 1)
    for i, q in enumerate(pts):
        bp = sp.bezier_points[i]
        bp.co = q
        bp.handle_left_type = bp.handle_right_type = 'AUTO'
    cu.bevel_depth = 0.022
    cu.bevel_resolution = 4
    o = bpy.data.objects.new('wire', cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat('w' + str(col), col, rough=0.35, coat=0.4))
    o.parent = root

# heartbeat trace floating above, like a trace lifted off the scope
def beat(t):
    v = 0.08 * math.exp(-((t - 0.2) / 0.035) ** 2)
    v += -0.09 * math.exp(-((t - 0.4) / 0.012) ** 2) + 0.75 * math.exp(-((t - 0.44) / 0.014) ** 2) - 0.18 * math.exp(-((t - 0.48) / 0.013) ** 2)
    v += 0.18 * math.exp(-((t - 0.7) / 0.05) ** 2)
    return v


pts = []
N = 600
for i in range(N):
    u = i / (N - 1)
    x = -2.4 + 4.8 * u
    t = (u * 2.4) % 1.0
    pts.append((x, 0.25, 0.95 + beat(t)))
cu = bpy.data.curves.new('trace', 'CURVE')
cu.dimensions = '3D'
sp = cu.splines.new('POLY')
sp.points.add(N - 1)
for i, q in enumerate(pts):
    sp.points[i].co = (*q, 1)
cu.bevel_depth = 0.022
cu.bevel_resolution = 4
tr = bpy.data.objects.new('trace', cu)
bpy.context.collection.objects.link(tr)
tr.data.materials.append(mat('green', (0.02, 0.55, 0.08), rough=0.25, coat=0.6, emit=(0.1, 1.0, 0.1), emit_strength=0.6))
tr.parent = root
cu2 = cu.copy()
cu2.bevel_depth = 0.045
tr2 = bpy.data.objects.new('halo', cu2)
bpy.context.collection.objects.link(tr2)
tr2.data.materials.append(mat('halo', (0, 0, 0), rough=1, emit=(0.1, 1.0, 0.05), emit_strength=0.25, alpha=0.12))
tr2.parent = root
tr2.hide_render = True
gl = bpy.data.lights.new('glow', 'AREA')
gl.energy = 60
gl.color = (0.4, 1.0, 0.3)
gl.size = 3.5
gl.size_y = 0.2
gl.shape = 'RECTANGLE'
glo = bpy.data.objects.new('glow', gl)
bpy.context.collection.objects.link(glo)
glo.location = (0, 0.25, 1.1)
glo.rotation_euler = (0, 0, 0)
glo.parent = root

fl = studio(z=0.0)
k = area('key', (-2.5, -3.0, 5.0), (0, 0, 0), 3.0, 260, (0.9, 0.93, 1.0))
r = area('rim', (3.0, 4.0, 2.5), (0, 0.5, 0), 3.0, 520, (0.6, 0.7, 1.0))
for l in (k, r):
    exclude(l, [fl])
camera((0.0, -6.2, 4.6), (0.0, 0.0, -0.15), lens=52, dof=7.6, fstop=4)
render(out)
