# extract_only.py
import numpy as np
import cv2
import pywt

def extract_message(image_path):
    """Extract binary message from stego image using DWT."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Khong the doc anh")

    coeffs = pywt.dwt2(img, 'haar')
    _, (cH, _, _) = coeffs

    cH_flat = cH.flatten()
    binary_length = ''
    for i in range(32):
        binary_length += '1' if cH_flat[i] >= 0 else '0'
    message_length = int(binary_length, 2)

    binary_message = ''
    for i in range(message_length):
        binary_message += '1' if cH_flat[i + 32] >= 0 else '0'

    return binary_message

if __name__ == "__main__":
    image_path = input("Nhap ten tep anh: ").strip()
    try:
        binary_msg = extract_message(image_path)
        with open("output.txt", "w") as f:
            f.write(binary_msg)
        print("Chuoi nhi phan nhan duoc:", binary_msg)
        print("Da trich xuat chuoi nhi phan vao file output.txt")
    except Exception as e:
        print("Loi:", str(e))
