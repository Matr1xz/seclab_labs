import pywt
import numpy as np
from PIL import Image
import logging

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def embed_watermark(image_path, watermark_path, output_path, strength=0.1):
    logger.info(f"Bắt đầu nhúng watermark vào ảnh: {image_path}")
    logger.info(f"Watermark: {watermark_path}, Output: {output_path}, Strength: {strength}")

    # Đọc ảnh gốc và chuyển sang grayscale
    logger.info("Đọc ảnh gốc và chuyển sang grayscale")
    img = Image.open(image_path).convert('L')
    img_array = np.array(img, dtype=np.float64)
    logger.info(f"Kích thước ảnh gốc: {img_array.shape}")

    # Đọc watermark và chuyển sang nhị phân
    logger.info("Đọc watermark")
    wm = Image.open(watermark_path).convert('L')
    logger.info(f"Kích thước watermark ban đầu: {wm.size}")
    
    # Áp dụng DWT cho ảnh gốc để lấy kích thước LL
    logger.info("Áp dụng DWT (wavelet: haar) cho ảnh gốc")
    coeffs = pywt.dwt2(img_array, 'haar')
    LL, (LH, HL, HH) = coeffs
    logger.info(f"Kích thước băng LL: {LL.shape}")

    # Resize watermark để khớp với kích thước LL
    logger.info("Resize watermark để khớp với kích thước băng LL")
    wm = wm.resize(LL.shape[::-1], Image.Resampling.LANCZOS)
    wm_array = np.array(wm, dtype=np.float64)
    wm_binary = (wm_array > 128).astype(np.float64)
    logger.info(f"Kích thước watermark sau resize: {wm_binary.shape}")

    # Nhúng watermark vào băng LL
    logger.info("Nhúng watermark vào băng LL")
    LL_watermarked = LL + strength * wm_binary * np.abs(LL).max()
    logger.debug(f"Giá trị max của LL trước nhúng: {np.abs(LL).max()}")

    # Tái tạo ảnh
    logger.info("Tái tạo ảnh bằng IDWT")
    coeffs_watermarked = (LL_watermarked, (LH, HL, HH))
    img_watermarked = pywt.idwt2(coeffs_watermarked, 'haar')
    img_watermarked = np.clip(img_watermarked, 0, 255).astype(np.uint8)
    logger.info(f"Kích thước ảnh sau tái tạo: {img_watermarked.shape}")

    # Lưu ảnh đã nhúng watermark
    logger.info(f"Lưu ảnh đã nhúng watermark tại: {output_path}")
    Image.fromarray(img_watermarked).save(output_path)
    logger.info("Hoàn tất quá trình nhúng watermark")

def extract_watermark(original_image_path, watermarked_image_path, output_wm_path):
    logger.info(f"Bắt đầu trích xuất watermark từ ảnh: {watermarked_image_path}")
    logger.info(f"Ảnh gốc: {original_image_path}, Output watermark: {output_wm_path}")

    # Đọc ảnh gốc và ảnh đã nhúng
    logger.info("Đọc ảnh gốc và ảnh đã nhúng")
    img_orig = Image.open(original_image_path).convert('L')
    img_wm = Image.open(watermarked_image_path).convert('L')
    img_orig_array = np.array(img_orig, dtype=np.float64)
    img_wm_array = np.array(img_wm, dtype=np.float64)
    logger.info(f"Kích thước ảnh gốc: {img_orig_array.shape}")
    logger.info(f"Kích thước ảnh đã nhúng: {img_wm_array.shape}")

    # Áp dụng DWT cho cả hai ảnh
    logger.info("Áp dụng DWT cho ảnh gốc và ảnh đã nhúng")
    coeffs_orig = pywt.dwt2(img_orig_array, 'haar')
    coeffs_wm = pywt.dwt2(img_wm_array, 'haar')
    LL_orig, _ = coeffs_orig
    LL_wm, _ = coeffs_wm
    logger.info(f"Kích thước băng LL (ảnh gốc): {LL_orig.shape}")
    logger.info(f"Kích thước băng LL (ảnh nhúng): {LL_wm.shape}")

    # Trích xuất watermark
    logger.info("Trích xuất watermark")
    wm_extracted = (LL_wm - LL_orig) / (np.abs(LL_orig).max() * 0.1)  # 0.1 là strength
    wm_extracted = np.clip(wm_extracted * 255, 0, 255).astype(np.uint8)
    logger.debug(f"Giá trị max của watermark trích xuất trước chuẩn hóa: {(LL_wm - LL_orig).max()}")

    # Lưu watermark trích xuất
    logger.info(f"Lưu watermark trích xuất tại: {output_wm_path}")
    Image.fromarray(wm_extracted).save(output_wm_path)
    logger.info("Hoàn tất quá trình trích xuất watermark")

# Sử dụng
image_path = 'input_image.png'  # Đường dẫn ảnh gốc
watermark_path = 'watermark.png'  # Đường dẫn ảnh watermark
output_path = 'watermarked_image.png'  # Đường dẫn ảnh đã nhúng
extracted_wm_path = 'extracted_watermark.png'  # Đường dẫn watermark trích xuất

# Nhúng watermark
embed_watermark(image_path, watermark_path, output_path, strength=0.1)

# Trích xuất watermark
extract_watermark(image_path, output_path, extracted_wm_path)