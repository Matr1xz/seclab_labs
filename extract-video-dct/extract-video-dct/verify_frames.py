import cv2
import numpy as np
import os
import glob

def compare_frames(original_dir, stego_dir):
    """So sánh khung hình gốc và khung hình nhúng."""
    original_files = sorted(glob.glob(os.path.join(original_dir, "*.png")), key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    stego_files = sorted(glob.glob(os.path.join(stego_dir, "*.png")), key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))

    if len(original_files) != len(stego_files):
        print(f"Error: Mismatch in number of frames. Original: {len(original_files)}, Stego: {len(stego_files)}")
        return

    print(f"Comparing {len(original_files)} frames...")
    differences = []

    for orig_file, stego_file in zip(original_files, stego_files):
        orig = cv2.imread(orig_file)
        stego = cv2.imread(stego_file)

        if orig is None or stego is None:
            print(f"Warning: Could not read {orig_file} or {stego_file}. Skipping.")
            continue

        diff = np.abs(orig.astype(float) - stego.astype(float)).mean()
        differences.append(diff)
        if diff > 1.0:
            print(f"Warning: Significant difference in {os.path.basename(orig_file)}: Mean diff = {diff:.2f}")

    avg_diff = np.mean(differences) if differences else 0
    print(f"Average pixel difference across all frames: {avg_diff:.2f}")
    if avg_diff > 1.0:
        print("Warning: Frames have noticeable changes, which may affect steganography.")

if __name__ == "__main__":
    original_dir = "output/frames"
    stego_dir = "output/stego_frames"
    compare_frames(original_dir, stego_dir)
