from PIL import Image
import numpy as np
import sys

def extract_pixel_matrix(image_path, output_txt_path):
    # Mở ảnh và chuyển sang grayscale
    img = Image.open(image_path).convert('L')
    
    # Chuyển ảnh thành ma trận 2D (không flatten)
    pixel_matrix = np.array(img)
    
    # Lưu ma trận vào file .txt
    with open(output_txt_path, 'w') as f:
        for row in pixel_matrix:
            # Ghi từng hàng, các giá trị cách nhau bằng khoảng trắng
            f.write(' '.join(map(str, row)) + '\n')
    print(f"Ma tran diem anh duoc luu vao {output_txt_path}")

extract_pixel_matrix(sys.argv[1], "graymatrix.txt")
