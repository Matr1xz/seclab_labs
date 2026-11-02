import cv2
import numpy as np
import pywt
import math

# Ham chuyen van ban thanh chuoi bit
def text_to_bits(text):
    # Chuyen van ban thanh danh sach bit
    bits = ''.join(format(ord(c), '08b') for c in text)
    return bits

# Ham tinh PSNR
def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

# Ham giau tin vao kenh chi dinh (R, G, hoac B)
def embed_message_to_channel(image_path, message, output_path, channel_idx):
    # Doc anh mau
    img = cv2.imread(image_path)
    if img is None:
        raise Exception("Khong the doc anh")

    # Lay kich thuoc anh goc
    original_height, original_width = img.shape[:2]

    # Dam bao kich thuoc anh chia het cho 2
    if original_height % 2 != 0 or original_width % 2 != 0:
        new_height = original_height - (original_height % 2)
        new_width = original_width - (original_width % 2)
        img = img[:new_height, :new_width]
        print(f"Da cat anh ve kich thuoc ({new_height}, {new_width}) de chia het cho 2")

    # Tach kenh chi dinh (0: B, 1: G, 2: R)
    channel = img[:, :, channel_idx].astype(np.float32)

    # Ap dung DWT
    coeffs = pywt.dwt2(channel, 'haar')
    cA, (cH, cV, cD) = coeffs

    # Chuyen thong diep thanh bit
    message_bits = text_to_bits(message)
    print(f"Chuoi bit goc (kenh {['B', 'G', 'R'][channel_idx]}): {message_bits}")
    bit_index = 0

    # Giau tin vao subband cD (HH)
    cD_flat = cD.flatten()
    for i in range(len(cD_flat)):
        if bit_index < len(message_bits):
            bit = int(message_bits[bit_index])
            cD_flat[i] = np.round(cD_flat[i])
            if bit == 1:
                cD_flat[i] = cD_flat[i] + 1.0
            else:
                cD_flat[i] = cD_flat[i] - 1.0
            bit_index += 1
        else:
            break

    # Kiem tra xem da nhung du thong diep chua
    if bit_index < len(message_bits):
        print(f"Canh bao: Khong du he so wavelet de nhung toan bo thong diep ({bit_index}/{len(message_bits)} bit)")

    # Dua cD_flat ve ma tran
    cD = cD_flat.reshape(cD.shape)

    # Tai tao anh tu DWT
    coeffs_modified = (cA, (cH, cV, cD))
    channel_stego = pywt.idwt2(coeffs_modified, 'haar')

    # Cat khop kich thuoc anh goc
    channel_stego = channel_stego[:img.shape[0], :img.shape[1]]

    # Dam bao gia tri pixel trong khoang [0, 255]
    channel_stego = np.clip(channel_stego, 0, 255).astype(np.uint8)

    # Cap nhat kenh trong anh
    img_stego = img.copy()
    img_stego[:, :, channel_idx] = channel_stego

    # Luu anh chua tin
    cv2.imwrite(output_path, img_stego, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    # Tinh PSNR
    psnr = calculate_psnr(img, img_stego)
    print(f"PSNR khi giau tin vao kenh {['B', 'G', 'R'][channel_idx]}: {psnr:.2f} dB")

    return img_stego

# Ham main de chay thu
if __name__ == "__main__":
    image_path = 'input_image.png'  # Duong dan anh goc
    message = "Hello World"  # Thong diep can giau

    # Thu giau tin vao kenh G (channel_idx = 1)
    embed_message_to_channel(image_path, message, 'stego_image_g.png', channel_idx=1)

    # Thu giau tin vao kenh R (channel_idx = 2)
    embed_message_to_channel(image_path, message, 'stego_image_r.png', channel_idx=2)