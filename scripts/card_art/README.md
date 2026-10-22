# Card art renders

Blender scenes for the 3D archive cards. Each script builds its scene from primitives (no downloaded models) and renders with Cycles.

```sh
python -m venv venv && venv/bin/pip install bpy fonttools brotli pillow
# ce.py needs a TTF copy of the site font next to it:
venv/bin/python -c "from fontTools.ttLib import TTFont; t=TTFont('../../fonts/instrument-sans-1.woff2'); t.flavor=None; t.save('instrument-sans-1.ttf')"
# still: out.png width height samples [turn], where turn is a fraction of a full rotation
venv/bin/python -I fnirs.py out.png 900 1600 160
```

Stills are 900×1600 (tall cards) or 900×1100 (regular cards), saved as WebP q80 in `images/cards/`. Every scene sits on the same grey studio floor (`studio()` in `common.py`), lit only by the world, so all cards share one background (about `#cfcfd0`).

Every 3D card has a turntable loop (`card.loop` in `content.json`) that plays while the card is hovered. `./loop.sh implant redcap-feedback-workflow` renders 90 frames at 540×960 and 20 samples, easing the object through a 120° arc, then encodes them as H.264 at 30 fps (CRF 24) playing middle, end, start, middle, so the clip loops without a jump. Use 540×660 for regular cards (edit the size in `loop.sh`). Output goes to `videos/cards/<slug>.mp4` plus a VP9 `.webm`. The page fetches a clip as its card nears the screen and plays it on hover; touch screens and reduced-motion settings keep the still.
