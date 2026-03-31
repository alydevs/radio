#!/usr/bin/env python3
# gen_playlists.py — run this as a cron job or at container start
import os, mutagen, re, sys

MUSIC_DIR = "/music"
OUTPUT_DIR = "/etc/liquidsoap/playlists"
FILTERS = [
    ("genre", "Rock - (Hard|Prog|Arena) Rock",       "/etc/liquidsoap/playlists/genre-rock.m3u"),
    ("genre", "Rock - (Alternative|Indie|Pop) Rock",       "/etc/liquidsoap/playlists/genre-altrock.m3u"),
    ("genre", "Electronic", "/etc/liquidsoap/playlists/genre-electronic.m3u"),
    ("mood",  "Meditative", "/etc/liquidsoap/playlists/mood-meditative.m3u"),
    ("mood",  "Love",       "/etc/liquidsoap/playlists/mood-love.m3u"),
]

def get_tag(tags, key):
    for k, v in tags.items():
        if k.lower() == key.lower():
            val = v[0] if isinstance(v, list) else str(v)
            return val.lower()
    return ""

os.makedirs(OUTPUT_DIR, exist_ok=True)

all_files = []
for root, dirs, files in os.walk(MUSIC_DIR):
    for f in files:
        if f.lower().endswith(('.mp3','.flac','.ogg','.opus','.m4a','.aac')):
            all_files.append(os.path.join(root, f))

for tag, pattern, outpath in FILTERS:
    matched = []
    for path in all_files:
        try:
            f = mutagen.File(path, easy=True)
            if f and re.search(pattern, get_tag(f.tags or {}, tag), re.I):
                matched.append(path)
        except Exception:
            pass
    with open(outpath, "w") as fh:
        fh.write("\n".join(matched))
    print(f"{outpath}: {len(matched)} tracks")
