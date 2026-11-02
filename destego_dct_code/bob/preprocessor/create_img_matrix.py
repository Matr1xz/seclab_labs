from PIL import Image
import numpy as np
import sys

def image_to_matrix(input_path, output_txt, block_size=8):
    image = Image.open(input_path).convert("L")

    height, width = image.size
    
    padded_height = (height // block_size + (height % block_size > 0)) * block_size
    padded_width = (width // block_size + (width % block_size > 0)) * block_size

    full_matrix = np.zeros((padded_height, padded_width), dtype=np.uint8)
    full_matrix[:height, :width] = image 

    np.savetxt(output_txt, full_matrix, fmt="%d")

    print(f"Chuyen thanh cong ma tran diem anh: '{output_txt}'.")

input_image_path = sys.argv[1]
output_txt_path = "image_matrix.txt"

image_to_matrix(input_image_path, output_txt_path)
