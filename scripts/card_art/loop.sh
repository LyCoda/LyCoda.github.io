#!/bin/sh
# loop.sh <scene> <slug>: render a 120-degree sweep and encode it as a seamless card loop.
# Frames play middle -> end -> start -> middle at 30 fps, so the clip loops without a jump.
set -e
cd "$(dirname "$0")"
k=$1; slug=$2; d=sweep/$k
mkdir -p "$d"
SWEEP=90,60 venv/bin/python -I "$k.py" "$PWD/$d/f%03d.png" 540 960 20
L=$d/list.txt; : > "$L"
for i in $(seq 45 89) $(seq 88 -1 1) $(seq 0 44); do printf "file 'f%03d.png'\nduration 0.0333333\n" "$i" >> "$L"; done
mkdir -p ../../videos/cards
ffmpeg -y -loglevel error -f concat -safe 0 -i "$L" -r 30 -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -movflags +faststart -an "../../videos/cards/$slug.mp4"
ffmpeg -y -loglevel error -f concat -safe 0 -i "$L" -r 30 -c:v libvpx-vp9 -b:v 0 -crf 38 -row-mt 1 -deadline good -cpu-used 2 -pix_fmt yuv420p -an "../../videos/cards/$slug.webm"
