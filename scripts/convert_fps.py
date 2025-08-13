#!/usr/bin/env python3
import argparse
import subprocess
import os
from pathlib import Path
import cv2

def parse_args():
    parser = argparse.ArgumentParser(description="Extract frames at 8 FPS for all videos.")
    parser.add_argument("--input_dir", type=str, default="/home/dylan/sound_diar/MUSIC_dataset/MUSIC21_solo_videos", help="Directory containing class folders with videos")
    parser.add_argument("--output_dir", type=str, default="/home/dylan/sound_diar/data/frames", help="Directory to save extracted frames")
    parser.add_argument("--fps", type=int, default=8, help="Target FPS for frame extraction")
    return parser.parse_args()

def get_video_fps(video_path):
    try:
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        return fps
    except:
        return 0

def extract_frames(video_path, output_dir, target_fps):
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-t", "20", # extract only first 20 seconds
        "-vf", f"fps={target_fps}",
        "-q:v", "2",  # quality
        os.path.join(str(output_dir), "%06d.jpg")
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"❌ Failed to extract frames from {video_path.name}: {result.stderr.decode()}")

def main():
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    video_exts = [".mp4", ".avi", ".mov", ".mkv", ".mp4.mkv"]

    video_paths = [f for f in input_dir.rglob("*") if f.is_file() and any(f.name.lower().endswith(ext) for ext in video_exts)]

    print(f"Found {len(video_paths)} videos.")

    for video_path in video_paths:
        category = video_path.parent.name
        video_id = video_path.stem.split(".")[0]  # strip double extensions

        # Check frame rate
        fps = get_video_fps(video_path)
        if fps < args.fps:
            print(f"⚠️ Skipping {video_path.name} (FPS {fps:.2f} < {args.fps})")
            continue

        save_dir = output_dir / category / video_id
        if save_dir.exists() and any(save_dir.glob("*.jpg")):
            print(f"⏭️ Already extracted: {category}/{video_id}")
            continue

        print(f"📥 Extracting: {category}/{video_id} at {args.fps} FPS")
        extract_frames(video_path, save_dir, args.fps)

if __name__ == "__main__":
    main()
