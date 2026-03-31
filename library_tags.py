#!/usr/bin/env python3
import os
import sys
import mutagen
from collections import Counter

def get_tags(path):
    try:
        f = mutagen.File(path, easy=True)
        if not f or not f.tags:
            return [], []
        
        def split_tag(tag_list):
            results = []
            for entry in tag_list:
                for part in entry.split(';'):
                    part = part.strip()
                    if part:
                        results.append(part)
            return results
        
        genres = split_tag(f.tags.get('genre', []))
        moods  = split_tag(f.tags.get('mood', []))
        return genres, moods
    except Exception:
        return [], []

def scan(music_dir):
    genre_counts = Counter()
    mood_counts  = Counter()

    for root, dirs, files in os.walk(music_dir):
        for filename in files:
            if not filename.lower().endswith(('.mp3', '.flac')):
                continue
            path = os.path.join(root, filename)
            genres, moods = get_tags(path)
            for g in genres:
                genre_counts[g] += 1
            for m in moods:
                mood_counts[m] += 1

    results = (
        [(count, f"genre:{name}") for name, count in genre_counts.items()] +
        [(count, f"mood:{name}")  for name, count in mood_counts.items()]
    )
    results.sort(key=lambda x: x[0], reverse=True)

    for count, label in results:
        print(f"{count:>6} {label}")

if __name__ == "__main__":
    music_dir = sys.argv[1] if len(sys.argv) > 1 else "/music"
    scan(music_dir)
