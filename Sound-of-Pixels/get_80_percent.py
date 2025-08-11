import json

# Load full data
with open('/home/dylan/sound_diar/MUSIC_dataset/MUSIC21_solo_videos.json', "r") as f:
    full_data = json.load(f)

# Load 20% subset
with open('/home/dylan/sound_diar/MUSIC_dataset/MUSIC21_solo_videos_20_percent.json', "r") as f:
    subset_20 = json.load(f)
remaining_videos = {}
for instrument, videos in full_data['videos'].items():
    subset_videos = set(subset_20['videos'].get(instrument, []))  # default to empty if missing
    full_videos = set(videos)

    # Keep only the videos not in the 20% subset
    remaining = full_videos - subset_videos

    if remaining:
        remaining_videos[instrument] = list(remaining)

# Print or save the 80% remaining

with open('/home/dylan/sound_diar/MUSIC_dataset/MUSIC21_solo_videos_80_percent.json', 'w') as f:
    print(json.dump({'videos': remaining_videos}, f, indent=2))