def message_to_binary(message):
    return binary_message

if __name__ == "__main__":
    # Read message from file input_message.txt
    input_file = "input_message.txt"
    try:
        with open(input_file, "r") as f:
            message = f.read().strip()
        if not message:
            print(f"Error: File {input_file} is empty or contains no valid text.")
            exit(1)
        print(f"Message read from {input_file}: {message}")
    except FileNotFoundError:
        print(f"Error: File {input_file} not found. Please create it and add your message.")
        exit(1)
    except Exception as e:
        print(f"Error reading file {input_file}: {e}")
        exit(1)

    # Convert message to binary string
    binary_message = message_to_binary(message)
    if binary_message:
        print("Message conversion successful.")
        with open("binary_message.txt", "w") as f:
            f.write(binary_message)
    else:
        print("Message conversion failed.")
