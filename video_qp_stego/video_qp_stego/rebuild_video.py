import os
import subprocess

def rebuild_video(temp_frame_pattern="temp_frame_{:04d}.mp4", total_frames=315,
                  fps=25.0, width=640, height=480,
                  output_video="output.mp4"):

    # Bước 1: Tạo file_list.txt cho FFmpeg concat
    with open("file_list.txt", "w") as f:
        for i in range(total_frames):
            temp_file = temp_frame_pattern.format(i+1)
            if os.path.exists(temp_file):
                f.write(f"file '{temp_file}'\n")
            else:
                print(f"Warning: Missing frame file {temp_file}")

    # Bước 2: Dùng FFmpeg để nối các đoạn video
    try:
        cmd = [
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'file_list.txt',
            '-c:v', 'libx264', '-qp', '22', '-r', str(fps),
            '-s', f'{width}x{height}', output_video
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Rebuilt video saved as: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg concat error: {e.stderr}")
        return False

    # Bước 3: So sánh kích thước với input (nếu có)
    if os.path.exists("input.mp4"):
        input_size = os.path.getsize("input.mp4") / (1024 * 1024)
        output_size = os.path.getsize(output_video) / (1024 * 1024)
        size_diff = abs(input_size - output_size)
        print(f"Input size:  {input_size:.2f} MB")
        print(f"Output size: {output_size:.2f} MB")
        print(f"Size diff:   {size_diff:.2f} MB")
        if size_diff < 1.0:
            print("✅ Size check passed (< 1MB)")
        else:
            print("❌ Size check failed (≥ 1MB)")

    # Bước 4: Dọn sạch file tạm
    for i in range(total_frames):
        temp_file = temp_frame_pattern.format(i+1)
        if os.path.exists(temp_file):
            os.remove(temp_file)
    if os.path.exists("file_list.txt"):
        os.remove("file_list.txt")

    return True

if __name__ == "__main__":
    if not os.path.exists("video_info.txt"):
        print("Missing video_info.txt")
        exit(1)
    with open("video_info.txt", "r") as f:
        lines = f.read().splitlines()
        fps = float(lines[0])
        total_frames = int(lines[1])
        width = int(lines[2])
        height = int(lines[3])

    rebuild_video(total_frames=total_frames, fps=fps, width=width, height=height)

