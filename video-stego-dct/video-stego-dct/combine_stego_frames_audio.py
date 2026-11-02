import subprocess
import argparse
import os
import sys
import glob

def check_dependencies():
    """Kiểm tra xem FFmpeg có được cài đặt không."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: FFmpeg is not installed. Install it using 'sudo apt install ffmpeg' on Ubuntu.")
        sys.exit(1)

def ensure_output_file(output_file):
    """Kiểm tra tệp đầu ra, hỏi người dùng nếu tệp đã tồn tại."""
    if os.path.exists(output_file):
        overwrite = input(f"The file '{output_file}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Operation canceled.")
            return False
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    return True

def combine_frames_audio(frames_dir, audio_path, output_path, fps=30):
    """Gộp các khung hình và âm thanh thành video MP4."""
    if not os.path.exists(frames_dir):
        print(f"Error: Frames directory '{frames_dir}' does not exist.")
        return False
    if not os.path.exists(audio_path):
        print(f"Error: Audio file '{audio_path}' does not exist.")
        return False
    if not ensure_output_file(output_path):
        return False

    # Kiểm tra khung hình
    frame_files = sorted(glob.glob(os.path.join(frames_dir, "*.png")), key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    if not frame_files:
        print(f"Error: No PNG frames found in '{frames_dir}'.")
        return False

    # Tạo video tạm thời từ khung hình
    temp_video = "output/temp_video.mp4"
    try:
        subprocess.run([
            "ffmpeg", "-framerate", str(fps), "-i", f"{frames_dir}/%d.png",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-y", temp_video
        ], check=True, capture_output=True, text=True)

        # Kết hợp video và âm thanh
        subprocess.run([
            "ffmpeg", "-i", temp_video, "-i", audio_path,
            "-c:v", "copy", "-c:a", "aac", "-shortest", "-y", output_path
        ], check=True, capture_output=True, text=True)

        print(f"Combined video saved to {output_path}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error combining frames/audio: {e.stderr}")
        return False
    finally:
        if os.path.exists(temp_video):
            os.remove(temp_video)

def main():
    check_dependencies()

    parser = argparse.ArgumentParser(description="Combine stego frames and audio into a video")
    parser.add_argument("--frames-dir", default="output/stego_frames", help="Directory containing stego PNG frames (default: output/stego_frames)")
    parser.add_argument("--audio", default="output/audio.wav", help="Input audio file (default: output/audio.wav)")
    parser.add_argument("--output", default="output/combined_video.mp4", help="Output video file (default: output/combined_video.mp4)")
    parser.add_argument("--fps", type=int, default=30, help="Frame rate for the output video (default: 30)")

    args = parser.parse_args()

    if not combine_frames_audio(args.frames_dir, args.audio, args.output, args.fps):
        sys.exit(1)

if __name__ == "__main__":
    main()
