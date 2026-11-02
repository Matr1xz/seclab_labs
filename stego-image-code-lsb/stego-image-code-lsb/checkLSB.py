from PIL import Image
import numpy as np

def check_lsb(original_path, stego_path, k):
    original_img = Image.open(original_path).convert('L')
    stego_img = Image.open(stego_path).convert('L')
    original_pixels = np.array(original_img).flatten()
    stego_pixels = np.array(stego_img).flatten()
    mask = 2**k - 1
    original_lsb = original_pixels & mask
    stego_lsb = stego_pixels & mask
    diff_lsb = original_lsb != stego_lsb
    num_diff = np.sum(diff_lsb)
    binary_message = ""
    for pixel in stego_pixels:
        lsb_bits = pixel & mask
        binary_message += format(lsb_bits, f'0{k}b')
    end_marker = '11111111'
    if end_marker in binary_message:
        binary_message = binary_message[:binary_message.index(end_marker)]
    else:
        binary_message = binary_message[:128]
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            message += chr(int(byte, 2))
    print(f"Thông điệp trích xuất: {message}")
    return message

extracted_message = check_lsb("input.png", "output.png", k=2)
