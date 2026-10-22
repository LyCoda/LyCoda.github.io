"""Route to a CE Mark: four glass risk-class pillars (I, IIa, IIb, III) rising in height.
No class is highlighted, so the card does not give away the quiz answer."""
import bpy, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

out, W, H, SPP, F = args()
reset(W, H, SPP, bg=(0.004, 0.008, 0.02))

root = bpy.data.objects.new('root', None)
bpy.context.collection.objects.link(root)
root.rotation_euler = (0, 0, math.radians(-28) + F * 2 * math.pi)

font = bpy.data.fonts.load(os.path.join(S, 'instrument-sans-1.ttf'))
labels = ['I', 'IIa', 'IIb', 'III']
heights = [0.9, 1.4, 1.9, 2.4]
glow = [(0.25, 0.5, 1.0), (0.3, 0.45, 1.0), (0.38, 0.4, 1.0), (0.48, 0.36, 1.0)]
pw, gap = 0.62, 0.16
x0 = -(4 * pw + 3 * gap) / 2 + pw / 2
objs = []
for i, (lab, h) in enumerate(zip(labels, heights)):
    x = x0 + i * (pw + gap)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, h / 2))
    p = bpy.context.object
    p.scale = (pw, pw, h)
    bpy.ops.object.transform_apply(scale=True)
    smooth(p, bevel=0.05, segments=8)
    assign(p, mat(f'g{i}', (0.35, 0.55, 1.0), rough=0.1, trans=1.0, ior=1.45, coat=1.0))
    p.parent = root
    objs.append(p)
    # glowing base plate inside the pillar
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0.03))
    b = bpy.context.object
    b.scale = (pw - 0.12, pw - 0.12, 0.03)
    bpy.ops.object.transform_apply(scale=True)
    assign(b, emission(f'b{i}', glow[i], 6))
    b.parent = root
    # thin light line at the top
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, h - 0.06))
    t = bpy.context.object
    t.scale = (pw - 0.14, pw - 0.14, 0.008)
    bpy.ops.object.transform_apply(scale=True)
    assign(t, emission(f't{i}', glow[i], 3))
    t.parent = root
    # label, floating in front of the face
    cu = bpy.data.curves.new(f'txt{i}', 'FONT')
    cu.body = lab
    cu.font = font
    cu.size = 0.36
    cu.extrude = 0.012
    cu.align_x = 'CENTER'
    cu.align_y = 'CENTER'
    tx = bpy.data.objects.new(f'txt{i}', cu)
    bpy.context.collection.objects.link(tx)
    tx.location = (x, -pw / 2 - 0.02, h - 0.32)
    tx.rotation_euler = (math.pi / 2, 0, 0)
    tx.data.materials.append(mat(f'tm{i}', (0.02, 0.05, 0.15), rough=0.3))
    tx.parent = root

# soft blue glow wall behind the pillars
bpy.ops.mesh.primitive_plane_add(size=1, location=(0.3, 1.5, 1.0), rotation=(math.pi / 2, 0, 0))
gw = bpy.context.object
gw.scale = (6, 5, 1)
gm = bpy.data.materials.new('gw'); gm.use_nodes = True
nt = gm.node_tree; nt.nodes.clear()
tc = nt.nodes.new('ShaderNodeTexCoord'); gr = nt.nodes.new('ShaderNodeTexGradient'); gr.gradient_type = 'QUADRATIC_SPHERE'
mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.6, 1.9, 1)
cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (0, 0, 0, 1); cr.color_ramp.elements[1].color = (0.12, 0.25, 1.0, 1); cr.color_ramp.elements[1].position = 1.0; cr.color_ramp.interpolation = 'EASE'
em = nt.nodes.new('ShaderNodeEmission'); em.inputs[1].default_value = 1.2
o = nt.nodes.new('ShaderNodeOutputMaterial')
nt.links.new(tc.outputs['Generated'], mp.inputs[0]); nt.links.new(mp.outputs[0], gr.inputs[0])
nt.links.new(gr.outputs['Fac'], cr.inputs[0]); nt.links.new(cr.outputs[0], em.inputs[0]); nt.links.new(em.outputs[0], o.inputs[0])
mp.inputs['Location'].default_value = (-0.8, -1.0, 0)
gw.data.materials.append(gm)
gw.hide_render = True
fl = studio(z=0.0)
k = area('key', (-2.6, -3.2, 5.2), (0, 0, 1), 2.4, 420, (0.85, 0.9, 1.0))
r = area('rim', (2.8, 3.2, 3.6), (0, 0, 1.0), 2.5, 600, (0.4, 0.5, 1.0))
s = area('strip', (-3.6, 1.4, 2.0), (0, 0, 1.2), 3.0, 260, (0.8, 0.85, 1.0), size_y=0.25)
for l in (k, r, s):
    exclude(l, [fl])
camera((-0.1, -8.4, 2.6), (-0.15, 0, 0.5), lens=42, dof=7.4, fstop=5.6)
render(out)
