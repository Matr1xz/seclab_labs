import sys

def binary_to_text(binary_str):
    if len(binary_str) % 8 != 0:
        print("Error: Binary string is not a valid.")
        return ""
    
    text = "".join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))
    return text
    
binary_input = sys.argv[1]
decoded_message = binary_to_text(binary_input)
print("The decoded message is:", decoded_message)
