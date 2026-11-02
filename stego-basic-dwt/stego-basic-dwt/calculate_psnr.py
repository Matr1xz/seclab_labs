import cv2
import numpy as np

def calculate_psnr(img1_path, img2_path):
    
    # Doc hai anh
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        raise ValueError("Khong the doc mot trong hai anh")

    if img1.shape != img2.shape:
        raise ValueError("Kich thuoc hai anh khong giong nhau")

    # Tinh MSE
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0: 
        return float('inf')

    # Tinh PSNR
    max_pixel = 255.0 
    psnr = 10 * np.log10((max_pixel ** 2) / mse)
    return psnr

if __name__ == "__main__":
    original_image = "input_image.jpg"
    stego_image = "stego.jpg"

    try:
        psnr_value = calculate_psnr(original_image, stego_image)
        print(f"PSNR giua {original_image} va {stego_image} la: {psnr_value:.2f} dB")
    except Exception as e:
        print("Loi:", str(e))
