from PIL import Image
import numpy as np
import sys 

def matrix_to_image(input_txt_path, output_image_path):
    # Đọc file newgraymatrix.txt và chuyển thành ma trận 2D
    matrix_2d = []
    with open(input_txt_path, 'r') as f:
        for line in f:
            # Tách các số trong dòng và chuyển thành int
            row = [int(num) for num in line.strip().split()]
            matrix_2d.append(row)
    
    # Chuyển ma trận thành mảng NumPy
    pixel_matrix = np.array(matrix_2d, dtype=np.uint8)
    
    # Tạo ảnh từ ma trận
    new_img = Image.fromarray(pixel_matrix, mode='L')
    
    # Lưu ảnh
    new_img.save(output_image_path)
    print(f"Da luu anh vao file {output_image_path}")

# Sử dụng
matrix_to_image(sys.argv[1], "output.png")
