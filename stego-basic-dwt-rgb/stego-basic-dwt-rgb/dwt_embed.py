import cv2
import numpy as np
import pywt

# Ham chuyen van ban thanh chuoi bit
def text_to_bits(text):
    # Chuyen van ban thanh danh sach bit
    bits = ''.join(format(ord(c), '08b') for c in text)
    return bits

# Ham giau tin vao kenh B
def embed_message(image_path, message, output_path):
    print("Dang giau tin...")
    
    # Doc anh mau
    img = cv2.imread(image_path)
    if img is None:
        raise Exception("Khong the doc anh")

    # Lay kich thuoc anh goc
    original_height, original_width = img.shape[:2]

    # Dam bao kich thuoc anh chia het cho 2 (yeu cau cua DWT)
    if original_height % 2 != 0 or original_width % 2 != 0:
        new_height = original_height - (original_height % 2)
        new_width = original_width - (original_width % 2)
        img = img[:new_height, :new_width]
        print(f"Da cat anh ve kich thuoc ({new_height}, {new_width}) de chia het cho 2")

    # Tach kenh B (Blue)
    b_channel = img[:, :, 0].astype(np.float32)  # Su dung float32 de dam bao chinh xac

    # Ap dung DWT len kenh B
    coeffs = pywt.dwt2(b_channel, 'haar')
    cA, (cH, cV, cD) = coeffs

    # Chuyen thong diep thanh bit
    message_bits = text_to_bits(message)
    print(f"Chuoi bit goc: {message_bits}")
    bit_index = 0

    # Giau tin vao subband cD (HH)
    cD_flat = cD.flatten()
    for i in range(len(cD_flat)):
        if bit_index < len(message_bits):
            # Nhung bit bang cach thay doi gia tri he so wavelet
            bit = int(message_bits[bit_index])
            cD_flat[i] = np.round(cD_flat[i])
            if bit == 1:
                cD_flat[i] = cD_flat[i] + 1.0  # Tang gia tri de dam bao bit 1
            else:
                cD_flat[i] = cD_flat[i] - 1.0  # Giam gia tri de dam bao bit 0
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
    b_channel_stego = pywt.idwt2(coeffs_modified, 'haar')

    # Cat khop kich thuoc anh goc
    b_channel_stego = b_channel_stego[:img.shape[0], :img.shape[1]]

    # Dam bao gia tri pixel trong khoang [0, 255]
    b_channel_stego = np.clip(b_channel_stego, 0, 255).astype(np.uint8)

    # Cap nhat kenh B trong anh
    img_stego = img.copy()
    img_stego[:, :, 0] = b_channel_stego

    # Luu anh chua tin voi PNG khong nen
    cv2.imwrite(output_path, img_stego, [cv2.IMWRITE_PNG_COMPRESSION, 0])

# Ham main de chay thu
if __name__ == "__main__":
    image_path = 'input_image.png'  # Duong dan anh goc (PNG)
    output_path = 'stego_image.png'  # Duong dan anh chua tin
    message = "Hello World! I'm PTIT student."  # Thong diep can giau
    embed_message(image_path, message, output_path)