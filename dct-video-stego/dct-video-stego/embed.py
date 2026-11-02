import numpy as np
import cv2
import argparse
from scipy.fft import dctn, idctn

BLOCK_SIZE = 8

def read_bits_from_file(file_path):
    with open(file_path, 'rb') as f:
        byte_data = f.read()
    payload = ''.join(f'{byte:08b}' for byte in byte_data)
    length_prefix = f'{len(payload):032b}'
    return length_prefix + payload

def embed_lsb(value, bit):
    value_int = int(round(value))
    if value_int % 2 != int(bit):
        value_int += 1 if bit == '1' else -1
    return float(value_int)

def embed_message(image, bitstream):
    h, w = image.shape
    dct_image = image.astype(np.float32)
    bit_idx = 0

    for i in range(0, h, BLOCK_SIZE):
        for j in range(0, w, BLOCK_SIZE):
            if bit_idx >= len(bitstream):
                break
            block = dct_image[i:i+BLOCK_SIZE, j:j+BLOCK_SIZE]
            if block.shape != (BLOCK_SIZE, BLOCK_SIZE):
                continue
            dct_block = dctn(block, type=2, norm='ortho')
            dct_block[1, 2] = embed_lsb(dct_block[1, 2], bitstream[bit_idx])
            dct_image[i:i+BLOCK_SIZE, j:j+BLOCK_SIZE] = idctn(dct_block, type=2, norm='ortho')
            bit_idx += 1
        if bit_idx >= len(bitstream):
            break

    print(f"number of bits embedded: {bit_idx} bit.")
    return np.clip(dct_image, 0, 255).astype(np.uint8)

def main():
    parser = argparse.ArgumentParser(description="Embed message into image")
    parser.add_argument("txtfilepath", help="Path to text file to embed")
    parser.add_argument("imagefilepath", help="Path to cover image")
    parser.add_argument("resultfilepath", help="Path to save stego image")
    args = parser.parse_args()

    image_color = cv2.imread(args.imagefilepath)
    ycrcb = cv2.cvtColor(image_color, cv2.COLOR_BGR2YCrCb)
    y = ycrcb[:, :, 0]

    bitstream = read_bits_from_file(args.txtfilepath)
    y_embedded = embed_message(y, bitstream)

    ycrcb[:, :, 0] = y_embedded
    final_image = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    cv2.imwrite(args.resultfilepath, final_image)

if __name__ == "__main__":
    main()

