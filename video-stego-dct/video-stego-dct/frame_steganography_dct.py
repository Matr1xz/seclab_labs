import cv2
import numpy as np
from scipy.fft import dct, idct
import argparse
import os
import sys
import glob
import shutil

def calculate_energy(dct_block):
    """Tính năng lượng của khối DCT (tổng bình phương hệ số, trừ DC)."""
    return np.sum(dct_block[1:]**2)

def string_to_binary(message):
    """Chuyển chuỗi thành dãy bit nhị phân."""
    return ''.join(format(ord(c), '08b') for c in message)

def binary_to_string(binary):
    """Chuyển dãy bit nhị phân thành chuỗi."""
    chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)]
    return ''.join(chars)

def embed_message(frame, binary_message, block_size=8, energy_threshold=10000, num_bits=1):
    """Nhúng thông điệp vào khung hình sử dụng DCT."""
    h, w = frame.shape[:2]
    msg_index = 0
    modified_blocks = 0

    # Chuyển sang YCrCb, chỉ xử lý kênh Y (độ sáng)
    frame_ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb).astype(float)

    for i in range(0, h - block_size + 1, block_size):
        for j in range(0, w - block_size + 1, block_size):
            if msg_index >= len(binary_message):
                break

            block = frame_ycrcb[i:i+block_size, j:j+block_size, 0]
            dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
            energy = calculate_energy(dct_block)

            if energy > energy_threshold:
                bits = binary_message[msg_index:msg_index+num_bits]
                msg_index += num_bits
                if len(bits) < num_bits:
                    bits = bits.ljust(num_bits, '0')

                for k, bit in enumerate(bits):
                    target_idx = (4 + k) % block_size
                    # Tăng cường thay đổi hệ số DCT
                    dct_block[target_idx, target_idx] = (abs(dct_block[target_idx, target_idx]) + 50) * (1 if bit == '1' else -1)

                block = idct(idct(dct_block.T, norm='ortho').T, norm='ortho')
                frame_ycrcb[i:i+block_size, j:j+block_size, 0] = np.clip(block, 0, 255)
                modified_blocks += 1

        if msg_index >= len(binary_message):
            break

    frame_bgr = cv2.cvtColor(frame_ycrcb.astype(np.uint8), cv2.COLOR_YCrCb2BGR)
    return frame_bgr, msg_index == len(binary_message), msg_index, modified_blocks

def hide_data(frames_dir, message_file, output_dir, num_bits, block_size=8, energy_threshold=10000):
    """Nhúng thông điệp từ message_file vào các khung hình và lưu tất cả khung hình."""
    if not os.path.exists(frames_dir):
        raise FileNotFoundError(f"Frames directory '{frames_dir}' does not exist.")
    if not os.path.exists(message_file):
        raise FileNotFoundError(f"Message file '{message_file}' does not exist.")

    # Tạo thư mục đầu ra
    if os.path.exists(output_dir):
        overwrite = input(f"The folder '{output_dir}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Operation canceled.")
            sys.exit(1)
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Đọc thông điệp
    with open(message_file, 'r') as f:
        message = f.read()
    binary_message = string_to_binary(message)

    # Đọc danh sách khung hình
    frame_files = sorted(glob.glob(os.path.join(frames_dir, "*.png")), key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    if not frame_files:
        raise ValueError("No PNG frames found in the specified directory.")

    print(f"Embedding message into {len(frame_files)} frames...")

    msg_index = 0
    frames_processed = 0
    total_modified_blocks = 0

    for frame_file in frame_files:
        frame = cv2.imread(frame_file)
        if frame is None:
            print(f"Warning: Could not read frame '{frame_file}'. Copying unchanged.")
            shutil.copy(frame_file, os.path.join(output_dir, os.path.basename(frame_file)))
            continue

        # Nhúng thông điệp nếu còn bit
        if msg_index < len(binary_message):
            frame, success, bits_embedded, modified_blocks = embed_message(frame, binary_message[msg_index:], block_size, energy_threshold, num_bits)
            msg_index += bits_embedded
            total_modified_blocks += modified_blocks
            if success:
                print(f"Message fully embedded after {frames_processed + 1} frames with {total_modified_blocks} modified blocks.")
        else:
            # Không cần nhúng, giữ nguyên khung hình
            pass

        # Lưu khung hình (đã nhúng hoặc không)
        output_file = os.path.join(output_dir, os.path.basename(frame_file))
        cv2.imwrite(output_file, frame)
        frames_processed += 1

    if msg_index < len(binary_message):
        print(f"Warning: Not enough high-energy blocks to embed the entire message. Embedded {msg_index}/{len(binary_message)} bits.")
    else:
        print(f"Message embedded successfully. All {frames_processed} stego frames saved to {output_dir} with {total_modified_blocks} modified blocks.")

def main():
    parser = argparse.ArgumentParser(description="Frame Steganography using DCT")
    parser.add_argument("command", choices=["hide", "recover"], help="Command to execute: 'hide' or 'recover'")
    parser.add_argument("--frames-dir", default="output/frames", help="Input directory containing PNG frames (default: output/frames)")
    parser.add_argument("--message", default="message.txt", help="Input message file for hiding (default: message.txt)")
    parser.add_argument("--output-dir", default="output/stego_frames", help="Output directory for stego frames (default: output/stego_frames)")
    parser.add_argument("--output", default="output/recovered.txt", help="Output file for recovered message (default: output/recovered.txt)")
    parser.add_argument("--num-bits", type=int, default=1, help="Number of bits to embed per block (default: 1)")
    parser.add_argument("--block-size", type=int, default=8, help="Block size for DCT (default: 8)")
    parser.add_argument("--energy-threshold", type=float, default=10000, help="Energy threshold for high-energy blocks (default: 10000)")
    parser.add_argument("--msg-length", type=int, default=23, help="Length of message to recover (default: 23 for 'Day la thong diep can giau')")

    args = parser.parse_args()

    if args.command == "hide":
        if not os.path.exists(args.message):
            print(f"Error: Message file '{args.message}' does not exist.")
            sys.exit(1)
        hide_data(args.frames_dir, args.message, args.output_dir, args.num_bits, args.block_size, args.energy_threshold)
    elif args.command == "recover":
        recover_data(args.frames_dir, args.output, args.msg_length, args.num_bits, args.block_size, args.energy_threshold)

def recover_data(frames_dir, output_file, msg_length, num_bits=1, block_size=8, energy_threshold=10000):
    """Trích xuất thông điệp từ các khung hình."""
    if not os.path.exists(frames_dir):
        raise FileNotFoundError(f"Frames directory '{frames_dir}' does not exist.")

    # Đọc danh sách khung hình
    frame_files = sorted(glob.glob(os.path.join(frames_dir, "*.png")), key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    if not frame_files:
        raise ValueError("No PNG frames found in the specified directory.")

    print(f"Extracting message from {len(frame_files)} frames...")

    binary_message = []
    max_bits = msg_length * 8

    for frame_file in frame_files:
        if len(binary_message) >= max_bits:
            break

        frame = cv2.imread(frame_file)
        if frame is None:
            print(f"Warning: Could not read frame '{frame_file}'. Skipping.")
            continue

        message_part = extract_message(frame, max_bits - len(binary_message), block_size, energy_threshold, num_bits)
        binary_message.extend(message_part)

    message = binary_to_string(''.join(binary_message[:max_bits]))

    # Lưu thông điệp trích xuất
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(message)
    print(f"Message recovered to {output_file}")

def extract_message(frame, max_bits, block_size=8, energy_threshold=10000, num_bits=1):
    """Trích xuất thông điệp từ khung hình."""
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
                    bit = '1' if dct_block[target_idx, target_idx] > 5 else '0'
                    binary_message.append(bit)
                    bits_extracted += 1
                    if bits_extracted >= max_bits:
                        break

        if bits_extracted >= max_bits:
            break

    return binary_message

def binary_to_string(binary):
    """Chuyển dãy bit nhị phân thành chuỗi."""
    chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)]
    return ''.join(chars)

if __name__ == "__main__":
    main()

