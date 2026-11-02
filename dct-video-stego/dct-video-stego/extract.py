import numpy as np
import cv2
import argparse
from scipy.fft import dctn

BLOCK_SIZE = 8

def extract_bit(value):
    return str(int(round(value)) % 2)

def extract_message(image_path):
    image_color = cv2.imread(image_path)
    ycrcb = cv2.cvtColor(image_color, cv2.COLOR_BGR2YCrCb)
    y = ycrcb[:, :, 0].astype(np.float32)

    h, w = y.shape
    bitstream = ''
    message_length = None
    total_needed = None

    for i in range(0, h, BLOCK_SIZE):
        for j in range(0, w, BLOCK_SIZE):
            block = y[i:i+BLOCK_SIZE, j:j+BLOCK_SIZE]
            if block.shape != (BLOCK_SIZE, BLOCK_SIZE):
                continue
            dct_block = dctn(block, type=2, norm='ortho')
            bit = extract_bit(dct_block[1, 2])
            bitstream += bit

            if message_length is None and len(bitstream) >= 32:
                message_length = int(bitstream[:32], 2)
                total_needed = 32 + message_length

            if total_needed and len(bitstream) >= total_needed:
                break
        if total_needed and len(bitstream) >= total_needed:
            break

    if not total_needed or len(bitstream) < total_needed:
        print("extraction failed.")
        return

    message_bits = bitstream[32:32+message_length]
    byte_data = [message_bits[i:i+8] for i in range(0, len(message_bits), 8)]
    recovered = bytes(int(b, 2) for b in byte_data)

    print("message extraxted:")
    print(recovered.decode(errors='replace'))

    with open("extracted_info.txt", "wb") as f:
        f.write(recovered)
    print("result saved in file: extracted_info.txt")

def main():
    parser = argparse.ArgumentParser(description="Extract message from stego image")
    parser.add_argument("watermarkedfilepath", help="Path to stego image")
    args = parser.parse_args()

    extract_message(args.watermarkedfilepath)

if __name__ == "__main__":
    main()

