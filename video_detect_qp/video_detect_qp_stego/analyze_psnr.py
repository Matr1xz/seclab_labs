# step4_analyze_psnr.py
import numpy as np
import os

# Đọc PSNR từ file
if not os.path.exists("psnr_values.txt"):
    print("Error: psnr_values.txt not found. Run step 3 first.")
    exit(1)

psnr_values = []
with open("psnr_values.txt", "r") as f:
    for line in f:
        psnr = float(line.strip())
        psnr_values.append(psnr)

if len(psnr_values) < 2:
    print("Error: Insufficient PSNR data to detect steganography.")
    exit(1)

std_dev_psnr = np.std(psnr_values)
mean_psnr = np.mean(psnr_values)
min_psnr = np.min(psnr_values)
max_psnr = np.max(psnr_values)
psnr_range = max_psnr - min_psnr

print(f"Inter-frame PSNR Statistics - Mean: {mean_psnr:.2f}, Std Dev: {std_dev_psnr:.2f}, Min: {min_psnr:.2f}, Max: {max_psnr:.2f}, Range: {psnr_range:.2f}")

# Lưu kết quả thống kê vào file
with open("psnr_stats.txt", "w") as f:
    f.write(f"Mean: {mean_psnr:.2f}\n")
    f.write(f"Std Dev: {std_dev_psnr:.2f}\n")
    f.write(f"Min: {min_psnr:.2f}\n")
    f.write(f"Max: {max_psnr:.2f}\n")
    f.write(f"Range: {psnr_range:.2f}\n")
print("PSNR statistics saved to psnr_stats.txt")
