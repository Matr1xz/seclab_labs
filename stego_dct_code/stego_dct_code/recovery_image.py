from PIL import Image
import numpy as np
import sys

def reconstruct_image_from_txt(input_file, output_image="recovered_image.png", original_image="input.png", block_size=8):

    original = Image.open(original_image).convert("L")
    
    height, width = original.size    

    full_matrix = np.loadtxt(input_file, dtype=np.uint8)

    final_image = full_matrix[:height, :width]

    image = Image.fromarray(final_image)
    
    image.save(output_image)
    print(f"Phuc hoi anh thanh cong: {output_image}")

input_file = sys.argv[1]

reconstruct_image_from_txt(input_file)
