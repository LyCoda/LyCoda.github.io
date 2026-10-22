import bpy, math, sys, os
from mathutils import Vector

S = os.path.dirname(os.path.abspath(__file__))


def args():
    a = sys.argv[1:]
    out = a[0]
    w, h = int(a[1]), int(a[2])
    samples = int(a[3]) if len(a) > 3 else 64
    frame = float(a[4]) if len(a) > 4 else 0.0  # turntable angle 0..1
    return out, w, h, samples, frame


def reset(w, h, samples, bg=(0.005, 0.006, 0.009), strength=1.0):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.max_bounces = 12
    sc.cycles.transmission_bounces = 12
    sc.cycles.glossy_bounces = 6
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGB'
    try:
        sc.view_settings.view_transform = 'AgX'
        sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception:
        pass
    world = bpy.data.worlds.new('W')
    sc.world = world
    world.use_nodes = True
    bgn = world.node_tree.nodes['Background']
    bgn.inputs[0].default_value = (*bg, 1)
    bgn.inputs[1].default_value = strength
    return sc


def mat(name, color=(0.8, 0.8, 0.8), metal=0.0, rough=0.4, trans=0.0, ior=1.45,
        emit=None, emit_strength=0.0, coat=0.0, sheen=0.0, alpha=1.0, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Metallic'].default_value = metal
    p.inputs['Roughness'].default_value = rough
    p.inputs['Transmission Weight'].default_value = trans
    p.inputs['IOR'].default_value = ior
    p.inputs['Coat Weight'].default_value = coat
    p.inputs['Sheen Weight'].default_value = sheen
    p.inputs['Alpha'].default_value = alpha
    if emit is not None:
        p.inputs['Emission Color'].default_value = (*emit, 1)
        p.inputs['Emission Strength'].default_value = emit_strength
    return m


def emission(name, color, strength):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission')
    e.inputs[0].default_value = (*color, 1)
    e.inputs[1].default_value = strength
    o = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(e.outputs[0], o.inputs[0])
    return m


def assign(obj, m):
    obj.data.materials.clear()
    obj.data.materials.append(m)
    return obj


def smooth(obj, bevel=None, segments=4, subsurf=0):
    if bevel:
        b = obj.modifiers.new('bev', 'BEVEL')
        b.width = bevel
        b.segments = segments
        b.limit_method = 'ANGLE'
    if subsurf:
        s = obj.modifiers.new('sub', 'SUBSURF')
        s.levels = s.render_levels = subsurf
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def area(name, loc, target, size, energy, color=(1, 1, 1), shape='RECTANGLE', size_y=None):
    l = bpy.data.lights.new(name, 'AREA')
    l.energy = energy
    l.color = color
    l.shape = shape
    l.size = size
    if size_y:
        l.size_y = size_y
    o = bpy.data.objects.new(name, l)
    bpy.context.collection.objects.link(o)
    o.location = loc
    look(o, target)
    return o


def look(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def camera(loc, target, lens=85, dof=None, fstop=2.8):
    c = bpy.data.cameras.new('Cam')
    c.lens = lens
    if dof is not None:
        c.dof.use_dof = True
        c.dof.focus_distance = dof
        c.dof.aperture_fstop = fstop
    o = bpy.data.objects.new('Cam', c)
    bpy.context.collection.objects.link(o)
    o.location = loc
    look(o, target)
    bpy.context.scene.camera = o
    return o


def backdrop(m, size=30, z=0.0, curve=True):
    """Seamless cyclorama: floor that sweeps up into a back wall."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, z))
    o = bpy.context.object
    if curve:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=40)
        bpy.ops.object.mode_set(mode='OBJECT')
        for v in o.data.vertices:
            y = v.co.y
            if y > 2:
                t = y - 2
                v.co.z += t * t * 0.12
        smooth(o)
    assign(o, m)
    return o


def render(out):
    _studio_links()
    sweep = os.environ.get('SWEEP')  # "frames,degrees": a sinusoidal turntable sweep instead of one still
    if not sweep:
        bpy.context.scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        return
    n, deg = sweep.split(',')
    n, amp = int(n), math.radians(float(deg))
    root = bpy.data.objects['root']
    base = root.rotation_euler.z
    bpy.context.scene.cycles.seed = 7
    for i in range(n):
        root.rotation_euler.z = base - amp * math.cos(math.pi * i / (n - 1))
        bpy.context.scene.render.filepath = out % i
        bpy.ops.render.render(write_still=True)


def exclude(light, objs):
    """Light linking: this light does not illuminate (or reflect in) the given objects."""
    c = bpy.data.collections.new('ex_' + light.name)
    for o in objs:
        c.objects.link(o)
    light.light_linking.receiver_collection = c
    for co in c.collection_objects:
        co.light_linking.link_state = 'EXCLUDE'


TONE = 1.15  # one grey for every card


def studio(z=0.0):
    """Shared grey sweep. Lit only by the grey world, so every card gets the same background."""
    w = bpy.context.scene.world.node_tree.nodes['Background']
    w.inputs[0].default_value = (TONE, TONE, TONE * 1.02, 1)
    w.inputs[1].default_value = 1.0
    m = mat('studio', (0.88, 0.88, 0.89), rough=0.5, spec=0.3)
    o = backdrop(m, size=40, z=z)
    o.name = 'studio'
    return o


def _studio_links():
    fl = bpy.data.objects.get('studio')
    if not fl:
        return
    for o in list(bpy.data.objects):
        if o.type == 'LIGHT' and o.data.type == 'AREA' and o.light_linking.receiver_collection is None:
            exclude(o, [fl])
