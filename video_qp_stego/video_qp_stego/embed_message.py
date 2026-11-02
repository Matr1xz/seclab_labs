import cv2
import numpy as np
import os
import subprocess

def detect_static_regions(prev_frame, curr_frame, threshold=2):
    diff = cv2.absdiff(prev_frame, curr_frame)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_diff, threshold, 1, cv2.THRESH_BINARY_INV)
    return mask

def embed_message(encoded_message):
    with open("video_info.txt") as f:
        fps, total_frames, width, height = map(float, f.read().splitlines())

    total_frames = int(total_frames)
    width = int(width)
    height = int(height)

    bit_index = 0
    embedded_frames = []
    prev_frame = None

    for i in range(total_frames):
        frame_file = f"frames/frame_{i+1:04d}.png"
        frame = cv2.imread(frame_file)
        qp_value = 28

        if bit_index < len(encoded_message) and prev_frame is not None:
            static_mask = detect_static_regions(prev_frame, frame)
            if np.sum(static_mask) > 0:
                bit = encoded_message[bit_index]
                qp_value = 28 if bit == '1' else 40
                embedded_frames.append(i)
                print(f"Frame {i+1}: Embedded bit {bit} → QP={qp_value}")
                bit_index += 1

        out_file = f"temp_frame_{i+1:04d}.mp4"
        cmd = [
            "ffmpeg", "-y", "-i", frame_file, "-c:v", "libx264",
            "-qp", str(qp_value), "-s", f"{width}x{height}", "-frames:v", "1", out_file
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        prev_frame = frame

    with open("file_list.txt", "w") as f:
        for i in range(total_frames):
            f.write(f"file 'temp_frame_{i+1:04d}.mp4'\n")
    with open("embedded_frames.txt", "w") as f:
        f.write("\n".join(map(str, embedded_frames)))
    print(f"Nhúng xong {bit_index} bit, danh sách ghi vào embedded_frames.txt")

if __name__ == "__main__":
    with open("encoded_message.txt") as f:
        encoded_message = f.read().strip()
    embed_message(encoded_message)

