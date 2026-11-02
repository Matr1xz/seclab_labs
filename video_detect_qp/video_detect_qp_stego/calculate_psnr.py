# step3_calculate_psnr.py
import os
import cv2
import numpy as np

extracted_dir = "extracted_frames"
num_frames = 315

# Đọc số khung hình từ file
if not os.path.exists("frame_count.txt"):
    print("Error: frame_count.txt not found. Run step 2 first.")
    exit(1)

with open("frame_count.txt", "r") as f:
    frame_count = int(f.read().strip())

def calculate_psnr(img1_path, img2_path):

psnr_values = []
for i in range(1, min(num_frames, frame_count)):
    frame1 = os.path.join(extracted_dir, f"extracted_frame_{i:04d}.png")
    frame2 = os.path.join(extracted_dir, f"extracted_frame_{i+1:04d}.png")
    if not os.path.exists(frame1) or not os.path.exists(frame2):
        print(f"Warning: Frame {i} or {i+1} missing: {frame1} or {frame2}. Skipping...")
        continue
    psnr = calculate_psnr(frame1, frame2)
    if psnr is not None:
        psnr_values.append(psnr)
        print(f"Frame {i} to {i+1}: PSNR = {psnr:.2f}")

# Lưu PSNR vào file để bước sau sử dụng
with open("psnr_values.txt", "w") as f:
    for i, psnr in enumerate(psnr_values, 1):
        f.write(f"{psnr}\n")
print(f"PSNR values saved to psnr_values.txt, total: {len(psnr_values)} values")
