import sys
from PIL import Image

def resize_image(input_path, output_path="img_gray.png", size=(512, 512)):
    try:
        img = Image.open(input_path) 
        img_gray = img.convert("L")  
        img_resized = img_gray.resize(size) 

        img_resized.save(output_path, format="PNG") 
        print(f"Tao anh thanh cong: {output_path}")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Loi cu phap.")
        sys.exit(1)

    input_image_path = sys.argv[1] 
    resize_image(input_image_path)

