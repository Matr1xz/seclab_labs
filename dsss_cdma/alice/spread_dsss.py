import numpy as np
import argparse
import os

# Hàm trải phổ tín hiệu
def spread_signal(user_data, gold_codes, N, K, sequence_length):
    """Trải phổ tín hiệu BPSK bằng Gold codes."""
    spreaded_signal = np.zeros((N, K * sequence_length))
    for i in range(N):
        spreaded_signal[i, :] = np.kron(user_data[i, :], gold_codes[i, :])
    return spreaded_signal

# Hàm đọc user_data và K từ file .txt
def load_bpsk_output(input_file):
    """Đọc user_data và K từ file .txt."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        K = None
        user_data = []
        for line in lines:
            line = line.strip()
            if line.startswith('K='):
                K = int(line.split('=')[1])
            elif line and not line.startswith('user_data='):
                user_data.append([int(x) for x in line.split()])

        user_data = np.array(user_data)
        if K is None or user_data.shape[1] != K:
            raise ValueError(f"Dữ liệu trong file {input_file} không hợp lệ")
        return user_data, K
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file {input_file}")
    except Exception as e:
        raise Exception(f"Lỗi khi đọc user_data từ {input_file}: {str(e)}")

# Hàm đọc gold_codes từ file .txt
def load_gold_codes(input_file):
    """Đọc gold_codes từ file .txt."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        gold_codes = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('gold_codes='):
                gold_codes.append([int(x) for x in line.split()])

        gold_codes = np.array(gold_codes)
        return gold_codes
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file {input_file}")
    except Exception as e:
        raise Exception(f"Lỗi khi đọc gold_codes từ {input_file}: {str(e)}")

# Hàm lưu spreaded_signal vào file .txt
def save_spread_output(spreaded_signal, output_file='spread_output.txt'):
    """Lưu spreaded_signal vào file .txt."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("spreaded_signal=\n")
            for i in range(spreaded_signal.shape[0]):
                spreaded_signal_str = ' '.join(map(str, spreaded_signal[i].astype(int)))
                f.write(f"{spreaded_signal_str}\n")
        print(f"Đã lưu spreaded_signal tại: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Lỗi khi lưu spreaded_signal: {str(e)}")

# Hàm chính
def main():
    # Thiết lập parser để nhận tham số dòng lệnh
    parser = argparse.ArgumentParser(description='Trải phổ tín hiệu.')
    parser.add_argument('-n','--N', type=int, required=True, help='Số lượng người dùng')
    parser.add_argument('-b','--bpsk_file', type=str, required=True, help='Đường dẫn đến file bpsk_output.txt')
    parser.add_argument('-g','--gold_codes_file', type=str, required=True, help='Đường dẫn đến file gold_codes_output.txt')
    args = parser.parse_args()

    N = args.N
    bpsk_file = args.bpsk_file
    gold_codes_file = args.gold_codes_file
    sequence_length = 127

    try:
        # Đọc user_data và K
        user_data, K = load_bpsk_output(bpsk_file)
        if user_data.shape[0] != N:
            raise ValueError(f"Số người dùng trong user_data ({user_data.shape[0]}) không khớp với N ({N})")

        # Đọc gold_codes
        gold_codes = load_gold_codes(gold_codes_file)
        if gold_codes.shape[0] != N or gold_codes.shape[1] != sequence_length:
            raise ValueError(f"Kích thước gold_codes không khớp: kỳ vọng ({N}, {sequence_length})")

        # Trải phổ tín hiệu
        spreaded_signal = spread_signal(user_data, gold_codes, N, K, sequence_length)
        print(spread_signal)
        print('Trai pho thanh cong')
        # Lưu kết quả
        save_spread_output(spreaded_signal)

    except Exception as e:
        print(f"Lỗi khi chạy chương trình: {str(e)}")

if __name__ == "__main__":
    main()
