import cv2
import os
import argparse
from moviepy.editor import VideoFileClip
from tqdm import tqdm
import sys
import shutil
from PIL import Image
import numpy as np

def check_dependencies():
    """Kiểm tra các thư viện cần thiết."""
    try:
        import cv2
        import moviepy.editor
        import tqdm
        import PIL
    except ImportError as e:
        print(f"Error: Missing library {e.name}. Install it using 'pip3 install {e.name.lower()}'")
        sys.exit(1)

def ensure_output_dir(output_dir):
    """Tạo thư mục đầu ra, hỏi người dùng nếu thư mục đã tồn tại."""
    if os.path.exists(output_dir):
        overwrite = input(f"The folder '{output_dir}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Operation canceled.")
            return False
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    return True

def ensure_output_file(output_file):
    """Kiểm tra tệp đầu ra, hỏi người dùng nếu tệp đã tồn tại."""
    if os.path.exists(output_file):
        overwrite = input(f"The file '{output_file}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Operation canceled.")
            return False
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    return True

def extract_frames(video_path, output_dir, max_frames=None):
    """Tách khung hình từ video và lưu dưới dạng PNG."""
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' does not exist.")
        return False

    if not ensure_output_dir(output_dir):
        return False

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video '{video_path}'.")
        return False

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if max_frames is not None:
        total_frames = min(total_frames, max_frames)

    success = True
    for index in tqdm(range(total_frames), desc="Extracting Frames"):
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: Could not read frame {index}. Stopping early.")
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img.save(os.path.join(output_dir, f"{index}.png"))

    cap.release()
    print(f"Frames saved to {output_dir}")
    return success

def extract_audio(video_path, output_audio_path):
    """Tách âm thanh từ video và lưu dưới dạng WAV."""
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' does not exist.")
        return False

    if not ensure_output_file(output_audio_path):
        return False

    try:
        video = VideoFileClip(video_path)
        if video.audio is None:
            print("Warning: Video has no audio track.")
            video.close()
            return False
        video.audio.write_audiofile(output_audio_path, codec='pcm_s16le')
        video.close()
        print(f"Audio saved to {output_audio_path}")
        return True
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return False

def main():
    check_dependencies()

    parser = argparse.ArgumentParser(description="Extract frames or audio from input.mp4")
    parser.add_argument("command", choices=["frames", "audio"], help="Command to execute: 'frames' or 'audio'")
    parser.add_argument("--video", default="input.mp4", help="Input video file (default: input.mp4)")
    parser.add_argument("--frames-dir", default="output/frames", help="Output directory for frames (default: output/frames)")
    parser.add_argument("--audio", default="output/audio.wav", help="Output audio file (default: output/audio.wav)")
    parser.add_argument("--max-frames", type=int, help="Maximum number of frames to extract (for 'frames')")

    args = parser.parse_args()

    if args.command == "frames":
        if not extract_frames(args.video, args.frames_dir, args.max_frames):
            sys.exit(1)
    elif args.command == "audio":
        if not extract_audio(args.video, args.audio):
            sys.exit(1)

if __name__ == "__main__":
    main()
