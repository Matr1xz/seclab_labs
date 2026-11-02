# binary_to_text.py
import sys

def binary_to_text(binary):
    """Convert binary string to text."""
    text = ''
    binary = binary[:len(binary) - len(binary) % 8]
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cach dung: python3 binary_to_text.py <ten_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, "r") as f:
            binary_data = f.read().strip()
        text = binary_to_text(binary_data)
        print("Thong diep duoc trich xuat:", text)
    except FileNotFoundError:
        print(f"Khong tim thay file: {input_file}")
    except Exception as e:
        print("Loi:", str(e))
