import cv2
import numpy as np
from scipy.fft import dct, idct
import argparse
import os
import sys
import glob
from tqdm import tqdm

def check_dependencies():
    """Kiểm tra các thư viện cần thiết."""
    try:
        import cv2
        import numpy
        import scipy.fft
        import tqdm
    except ImportError as e:
        print(f"Error: Missing library {e.name}. Install it using 'pip3 install {e.name.lower()}'")
        sys.exit(1)

def calculate_energy(dct_block):
    """Tính năng lượng của khối DCT (tổng bình phương hệ số, trừ DC)."""
    return np.sum(dct_block[1:]**2)

def binary_to_string(binary):
    """Chuyển dãy bit nhị phân thành chuỗi."""
    if len(binary) < 8:
        return ""
    chars = []
    for i in range(0, len(binary) - 7, 8):
        try:
            chars.append(chr(int(binary[i:i+8], 2)))
        except ValueError:
            break
    return ''.join(chars)

def extract_message(frame, max_bits, block_size=8, energy_threshold=10000, num_bits=1):
    """Trích xuất dãy bit thô từ khung hình."""
    h, w = frame.shape[:2]
    binary_message = []
    bits_extracted = 0

    frame_ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    for i in range(0, h - block_size + 1, block_size):
        for j in range(0, w - block_size + 1, block_size):
            if bits_extracted >= max_bits:
                break

            block = frame_ycrcb[i:i+block_size, j:j+block_size, 0].astype(float)
            dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
            energy = calculate_energy(dct_block)

            if energy > energy_threshold:
                for k in range(num_bits):
                    target_idx = (4 + k) % block_size
                    bit = '1' if dct_block[target_idx, target_idx] > 0 else '0'
                    binary_message.append(bit)
                    bits_extracted += 1
                    if bits_extracted >= max_bits:
                        break

        if bits_extracted >= max_bits:
            break

    return binary_message

def recover_data(frames_dir, output_file, msg_length, original_message_file=None, num_bits=1, block_size=8, energy_threshold=10000):
    """Trích xuất thông điệp từ tất cả khung hình trong thư mục."""
    if not os.path.exists(frames_dir):
        raise FileNotFoundError(f"Frames directory '{frames_dir}' does not exist.")

    # Đọc danh sách khung hình
    frame_files = sorted(glob.glob(os.path.join(frames_dir, "*.png")), key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    if not frame_files:
        raise ValueError("No PNG frames found in the specified directory.")

    print(f"Extracting message from {len(frame_files)} frames...")

    binary_message = []
    max_bits = msg_length * 8

    for frame_file in tqdm(frame_files, desc="Processing Frames"):
        if len(binary_message) >= max_bits:
            break

        frame = cv2.imread(frame_file)
        if frame is None:
            print(f"Warning: Could not read frame '{frame_file}'. Skipping.")
            continue

        binary_message.extend(extract_message(frame, max_bits - len(binary_message), block_size, energy_threshold, num_bits))

    if len(binary_message) < max_bits:
        print(f"Warning: Only extracted {len(binary_message)} bits, needed {max_bits} bits.")
        return

    # Chuyển bit thành chuỗi
    message = binary_to_string(''.join(binary_message[:max_bits]))

    # Lưu thông điệp trích xuất
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(message)
    print(f"Message recovered to {output_file}")

    # So sánh với thông điệp gốc nếu được cung cấp
    if original_message_file and os.path.exists(original_message_file):
        with open(original_message_file, 'r') as f:
            original_message = f.read()
        if message == original_message:
            print("Success: Recovered message matches the original message!")
        else:
            print("Warning: Recovered message does not match the original message.")
            print(f"Recovered: {message}")
            print(f"Original: {original_message}")

def main():
    check_dependencies()

    parser = argparse.ArgumentParser(description="Recover hidden message 'Day la thong diep can giau' from all stego frames using DCT")
    parser.add_argument("--frames-dir", default="output/stego_frames", help="Input directory containing stego PNG frames (default: output/stego_frames)")
    parser.add_argument("--output", default="output/recovered.txt", help="Output file for recovered message (default: output/recovered.txt)")
    parser.add_argument("--original-message", default="message.txt", help="Original message file for verification (default: message.txt)")
    parser.add_argument("--msg-length", type=int, default=23, help="Length of message to recover (default: 23 for 'Day la thong diep can giau')")
    parser.add_argument("--num-bits", type=int, default=1, help="Number of bits embedded per block (default: 1)")
    parser.add_argument("--block-size", type=int, default=8, help="Block size for DCT (default: 8)")
    parser.add_argument("--energy-threshold", type=float, default=10000, help="Energy threshold for high-energy blocks (default: 10000)")

    args = parser.parse_args()

    try:
        recover_data(args.frames_dir, args.output, args.msg_length, args.original_message, args.num_bits, args.block_size, args.energy_threshold)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
