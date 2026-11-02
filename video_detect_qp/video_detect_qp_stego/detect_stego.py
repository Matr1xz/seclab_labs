# step5_detect_stego.py
import os
threshold_std = 3.0
threshold_range = 8.0

# Đọc thống kê từ file
if not os.path.exists("psnr_stats.txt"):
    print("Error: psnr_stats.txt not found. Run step 4 first.")
    exit(1)

stats = {}
with open("psnr_stats.txt", "r") as f:
    for line in f:
        key, value = line.split(": ")
        stats[key] = float(value.strip())

std_dev_psnr = stats["Std Dev"]
psnr_range = stats["Range"]

is_stego = std_dev_psnr > threshold_std or psnr_range > threshold_range
if is_stego:
    print("Evidence of QP-based steganography detected: Significant inter-frame PSNR variation.")
else:
    print("No evidence of QP-based steganography detected: Inter-frame PSNR variation is normal.")

# Lưu kết quả
with open("detection_result.txt", "w") as f:
    f.write(f"Steganography detected: {is_stego}\n")
    f.write(f"Inter-frame PSNR Std Dev: {std_dev_psnr:.2f}\n")
    f.write(f"Inter-frame PSNR Range: {psnr_range:.2f}\n")
    f.write(f"Threshold Std: {threshold_std}, Threshold Range: {threshold_range}\n")
print("Detection result saved to detection_result.txt")
