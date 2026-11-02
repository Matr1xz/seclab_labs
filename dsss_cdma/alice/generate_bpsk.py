import numpy as np
import argparse
import os

# Hàm đọc thông điệp từ file .txt
def read_message_from_file(file_path):
    """Đọc nội dung từ file .txt và chuyển thành chuỗi bit."""
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            message = file.read()
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        return binary_message
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='utf-16') as file:
                message = file.read()
            binary_message = ''.join(format(ord(char), '08b') for char in message)
            return binary_message
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='windows-1252') as file:
                    message = file.read()
                binary_message = ''.join(format(ord(char), '08b') for char in message)
                return binary_message
            except UnicodeDecodeError:
                print(f"Không thể đọc file {file_path}. Sử dụng thông điệp mặc định.")
                return ''.join(format(ord(char), '08b') for char in "Default message")
    except FileNotFoundError:
        print(f"Không tìm thấy file {file_path}. Sử dụng thông điệp mặc định.")
        return ''.join(format(ord(char), '08b') for char in "Default message")

# Hàm tạo tín hiệu BPSK
def generate_bpsk_symbols(N, file_paths):
    """Tạo tín hiệu BPSK cho N người dùng từ các file .txt, tự động tính K."""
    binary_messages = []
    message_lengths = []

    for i in range(N):
        binary_message = read_message_from_file(file_paths[i])
        binary_messages.append(binary_message)
        message_lengths.append(len(binary_message))

    K = max(message_lengths)
    user_data = np.zeros((N, K))
    for i in range(N):
        binary_message = binary_messages[i]
        if len(binary_message) < K:
            binary_message = binary_message + '0' * (K - len(binary_message))
        bits = np.array([int(b) for b in binary_message])
        user_data[i, :] = bits * 2 - 1
    return user_data, K

# Hàm lưu user_data và K vào file .txt
def save_bpsk_output(user_data, K, output_file='bpsk_output.txt'):
    """Lưu user_data và K vào file .txt."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"K={K}\n")
            f.write("user_data=\n")
            for i in range(user_data.shape[0]):
                user_data_str = ' '.join(map(str, user_data[i].astype(int)))
                f.write(f"{user_data_str}\n")
        print(f"Đã lưu user_data và K tại: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Lỗi khi lưu user_data: {str(e)}")

# Hàm chính
def main():
    # Thiết lập parser để nhận tham số dòng lệnh
    parser = argparse.ArgumentParser(description='Tạo tín hiệu BPSK từ các file thông điệp.')
    parser.add_argument('-n','--N', type=int, required=True, help='Số lượng người dùng')
    parser.add_argument('-f','--file_paths', nargs='+', required=True, help='Danh sách các file .txt chứa thông điệp')
    args = parser.parse_args()

    N = args.N
    file_paths = args.file_paths

    # Kiểm tra số file_paths khớp với N
    if len(file_paths) != N:
        raise ValueError(f"Số file_paths ({len(file_paths)}) không khớp với N ({N})")

    try:
        # Tạo tín hiệu BPSK
        user_data, K = generate_bpsk_symbols(N, file_paths)
        print(f"Độ dài thông điệp (K): {K} bits")
        print(user_data)
        # Lưu kết quả
        save_bpsk_output(user_data, K)

    except Exception as e:
        print(f"Lỗi khi chạy chương trình: {str(e)}")

if __name__ == "__main__":
    main()
