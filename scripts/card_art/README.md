# Card art renders

Blender scenes for the 3D archive cards. Each script builds its scene from primitives (no downloaded models) and renders with Cycles.

```sh
python -m venv venv && venv/bin/pip install bpy fonttools brotli pillow
# ce.py needs a TTF copy of the site font next to it:
venv/bin/python -c "from fontTools.ttLib import TTFont; t=TTFont('../../fonts/instrument-sans-1.woff2'); t.flavor=None; t.save('instrument-sans-1.ttf')"
# still: out.png width height samples [turn], where turn is a fraction of a full rotation
venv/bin/python -I fnirs.py out.png 900 1600 160
```

Stills are 900×1600 (tall cards) or 900×1100 (regular cards), saved as WebP q80 in `images/cards/`. Turntable sprites are 9 frames at 540×960, 20 samples, turns from −32° to +32°, joined left to right and saved as WebP q74 in `images/cards/spin/`.
