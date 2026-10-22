"""Surgical Data Science: three clusters of glossy spheres floating over a white studio floor.
A symbolic picture of grouping data; positions are random, not from the coursework."""
import bpy, math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from mathutils import Vector

out, W, H, SPP, F = args()
sc = reset(W, H, SPP, bg=(0.9, 0.91, 0.93), strength=0.45)
sc.view_settings.look = 'AgX - Punchy'
random.seed(11)

root = bpy.data.objects.new('root', None)
bpy.context.collection.objects.link(root)
root.rotation_euler = (0, 0, F * 2 * math.pi)

palettes = [
    ((0.02, 0.22, 1.0), (-0.95, 0.25, 1.25)),
    ((1.0, 0.3, 0.02), (0.75, 0.45, 1.35)),
    ((0.95, 0.05, 0.32), (0.1, -0.5, 0.62)),
]
placed = []
for ci, (col, c) in enumerate(palettes):
    gloss = mat(f'gloss{ci}', col, rough=0.18, coat=1.0)
    satin = mat(f'satin{ci}', col, rough=0.45)
    glass = mat(f'glass{ci}', tuple(0.15 + 0.85 * v for v in col), rough=0.02, trans=1.0, ior=1.5)
    n = 0
    while n < 16:
        r = random.choice((0.035, 0.05, 0.06, 0.08, 0.1, 0.13)) * (1.4 if n == 0 else 1)
        off = Vector((random.gauss(0, 0.19), random.gauss(0, 0.19), random.gauss(0, 0.16)))
        p = Vector(c) + off
        if any((p - q).length < r + qr + 0.02 for q, qr in placed):
            continue
        placed.append((p, r))
        n += 1
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=r, location=p)
        s = bpy.context.object
        smooth(s)
        assign(s, random.choice((gloss, gloss, satin, glass)))
        s.parent = root

floor = mat('floor', (0.88, 0.89, 0.91), rough=0.5, spec=0.3)
backdrop(floor, size=40, z=0.0)
area('key', (-2.5, -3.0, 5.0), (0, 0, 1.0), 4.0, 420)
area('fill', (4.0, -3.0, 2.0), (0, 0, 1.0), 4.0, 110, (0.95, 0.97, 1.0))
area('back', (0.5, 5.0, 3.0), (0.5, 8, 1.5), 6.0, 900)
area('back2', (0.5, 4.0, 3.5), (0, 0, 1.0), 3.0, 160)
camera((0.9, -6.6, 2.1), (0.0, 0, 0.6), lens=52, dof=6.6, fstop=4)
render(out)
