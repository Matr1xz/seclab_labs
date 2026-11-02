def hamming_encode(data_bits):
    """Hamming (7,4) encoding for 4 data bits."""
    encoded = []
    for i in range(0, len(data_bits), 4):
        if i + 3 < len(data_bits):
            bits = data_bits[i:i+4]
            parity1 = int(bits[0]) ^ int(bits[1]) ^ int(bits[3])
            parity2 = int(bits[0]) ^ int(bits[2]) ^ int(bits[3])
            parity3 = int(bits[1]) ^ int(bits[2]) ^ int(bits[3])
            encoded.extend([parity1, parity2, bits[0], parity3, bits[1], bits[2], bits[3]])
    return ''.join(map(str, encoded))

def encode_binary_message(binary_message):
    print("Starting Hamming encoding...")
    encoded_message = hamming_encode(binary_message)
    print(f"Hamming encoded binary string: {encoded_message} ({len(encoded_message)} bit)")
    print("Step 2B completed: Message has been Hamming encoded.")
    return encoded_message

if __name__ == "__main__":
    with open("binary_message.txt", "r") as f:
        binary_message = f.read().strip()
    encoded_message = encode_binary_message(binary_message)
    if encoded_message:
        print("Hamming encoding successful.")
        with open("encoded_message.txt", "w") as f:
            f.write(encoded_message)
            print("File encoded_message.txt created successfully.")  
    else:
        print("Hamming encoding failed.")
