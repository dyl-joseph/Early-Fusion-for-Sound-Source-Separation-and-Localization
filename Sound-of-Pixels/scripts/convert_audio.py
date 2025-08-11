#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

def arg_parse():
    parser = argparse.ArgumentParser(description="Extract audio from videos into 11025Hz mono MP3 files.")
    parser.add_argument("--input_dir", type=str, default="/home/dylan/sound_diar/MUSIC_dataset/MUSIC21_solo_videos", help="Directory with original video files")
    parser.add_argument("--output_dir", type=str, default="/home/dylan/sound_diar/data/audio", help="Directory to save converted MP3 files")
    parser.add_argument("--sr", type=int, default=11025, help="Target sample rate")
    return parser.parse_args()

def is_video_file(file_path):
    VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".webm"]
    return any(ext in file_path.name.lower() for ext in VIDEO_EXTENSIONS)

def convert_audio_files(input_dir, output_dir, target_sr=11025):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.exists():
        print(f"ERROR: Input directory {input_dir} does not exist!")
        return

    video_files = [f for f in input_dir.rglob("*") if f.is_file() and is_video_file(f)]
    print(f"🔍 Found {len(video_files)} video files to process")

    for video_path in video_files:
        instrument = video_path.parent.name
        base_id = video_path.stem.split('.')[0]  # Remove extra extensions like ".mp4.mkv"

        output_category_dir = output_dir / instrument
        output_category_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_category_dir / f"{base_id}.mp3"

        cmd = [
            "ffmpeg", "-y", "-i", str(video_path),
            "-t", "20", # 20 seconds
            "-ar", str(target_sr),
            "-ac", "1",
            "-c:a", "mp3",
            "-b:a", "128k",
            str(output_path)
        ]

        print(f"🎧 Converting {video_path} → {output_path}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"❌ Error converting {video_path}:\n{result.stderr}")

if __name__ == "__main__":
    args = arg_parse()
    convert_audio_files(args.input_dir, args.output_dir, args.sr)
