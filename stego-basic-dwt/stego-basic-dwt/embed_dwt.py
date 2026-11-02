import numpy as np
from PIL import Image
import pywt
import cv2

def text_to_binary(text):
    """Convert text to binary string."""
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def embed_message(image_path, message, output_path):
    """Hide message in image using DWT."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Khong the doc anh")

    binary_message = text_to_binary(message)
    message_length = len(binary_message)
    binary_length = format(message_length, '032b')

    coeffs = pywt.dwt2(img, 'haar')
    cA, (cH, cV, cD) = coeffs

    cH_flat = cH.flatten()
    if len(cH_flat) < message_length + 32:
        raise ValueError("Anh qua nho de chua thong diep!")

    for i in range(32):
        cH_flat[i] = cH_flat[i] + (10 if binary_length[i] == '1' else -10)

    for i in range(message_length):
        cH_flat[i + 32] = cH_flat[i + 32] + (10 if binary_message[i] == '1' else -10)

    cH = cH_flat.reshape(cH.shape)

    coeffs_modified = (cA, (cH, cV, cD))
    img_stego = pywt.idwt2(coeffs_modified, 'haar')

    img_stego = np.clip(img_stego, 0, 255).astype(np.uint8)
    img_stego = Image.fromarray(img_stego)
    img_stego.save(output_path, 'JPEG', quality=100)
    return message_length

if __name__ == "__main__":
    input_image = "input_image.jpg"
    output_image = "stego.jpg"
    secret_message = "This is a secret message!"

    try:
        message_length = embed_message(input_image, secret_message, output_image)
        print("Da nhung thong diep thanh cong!")
        print(f"Do dai thong diep: {message_length} bits")
    except Exception as e:
        print("Loi:", str(e))