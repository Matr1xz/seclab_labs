import cv2
import numpy as np
import math

# Ham tinh PSNR
def calculate_psnr(img1, img2, channel=None):
    # Kiem tra va dieu chinh kich thuoc anh
    height1, width1 = img1.shape[:2]
    height2, width2 = img2.shape[:2]
    min_height = min(height1, height2)
    min_width = min(width1, width2)
    
    # Cat anh de co cung kich thuoc
    img1 = img1[:min_height, :min_width]
    img2 = img2[:min_height, :min_width]
    
    # Neu channel duoc chi dinh, chi tinh PSNR cho kenh do
    if channel is not None:
        img1 = img1[:, :, channel]
        img2 = img2[:, :, channel]
    
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

# Ham main de chay thu
if __name__ == "__main__":
    original_image_path = 'input_image.png'  # Duong dan anh goc
    stego_image_path = 'stego_image.png'  # Duong dan anh chua tin

    # Doc anh
    img_original = cv2.imread(original_image_path)
    img_stego = cv2.imread(stego_image_path)
    
    if img_original is None or img_stego is None:
        raise Exception("Khong the doc anh")

    # Tinh PSNR tong the
    psnr_total = calculate_psnr(img_original, img_stego)
    print(f"PSNR tong the giua anh goc va anh chua tin: {psnr_total:.2f} dB")

    # Tinh PSNR cho kenh B (channel 0)
    psnr_b = calculate_psnr(img_original, img_stego, channel=0)
    print(f"PSNR kenh B giua anh goc va anh chua tin: {psnr_b:.2f} dB")