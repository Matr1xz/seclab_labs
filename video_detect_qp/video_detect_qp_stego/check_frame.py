import os
# step2_check_frames.py
extracted_dir = "extracted_frames"
num_frames = 315

# Đọc số khung hình từ file
if not os.path.exists("frame_count.txt"):
    print("Error: frame_count.txt not found. Run step 1 first.")
    exit(1)

with open("frame_count.txt", "r") as f:
    frame_count = int(f.read().strip())

print(f"Number of frames extracted: {frame_count}")
if frame_count < num_frames:
    print(f"Warning: Only {frame_count} frames extracted, expected {num_frames}. Proceeding with available frames.")
else:
    print("Enough frames extracted.")

if frame_count < 2:
    print("Error: Insufficient frames to proceed.")
    exit(1)
