import cv2
import numpy as np
import pywt

# Ham chuyen chuoi bit thanh van ban
def bits_to_text(bits):
    # Chuyen danh sach bit thanh van ban
    try:
        chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
        return ''.join(chars)
    except ValueError:
        return "Loi khi chuyen bit thanh van ban"

# Ham trich xuat thong diep tu kenh B
def extract_message(stego_image_path, message_length):
    # Doc anh chua tin
    img_stego = cv2.imread(stego_image_path)
    if img_stego is None:
        raise Exception("Khong the doc anh chua tin")

    # Tach kenh B
    b_channel = img_stego[:, :, 0].astype(np.float32)  # Su dung float32

    # Ap dung DWT
    coeffs = pywt.dwt2(b_channel, 'haar')
    _, (_, _, cD) = coeffs

    # Trich xuat bit tu subband cD
    cD_flat = cD.flatten()
    extracted_bits = ''
    for i in range(min(len(cD_flat), message_length * 8)):
        # Trich xuat dua tren gia tri he so
        extracted_bits += '1' if cD_flat[i] > 0 else '0'

    # Chuyen bit thanh van ban
    extracted_message = bits_to_text(extracted_bits)
    return extracted_message, extracted_bits

# Ham main de chay thu
if __name__ == "__main__":
    stego_image_path = 'stego_image.png'  # Duong dan anh chua tin
    message_length = 30 
    extracted_message, extracted_bits = extract_message(stego_image_path, message_length)
    print(f"Thong diep trich xuat: {extracted_message}")
    print(f"Chuoi bit trich xuat: {extracted_bits[:message_length*8]}")