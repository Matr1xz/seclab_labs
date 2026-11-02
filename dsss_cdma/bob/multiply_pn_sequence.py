import numpy as np
import argparse
import os

# Hàm đọc parallel_signal từ file .txt
def load_parallel_signal(input_file, N, K, sequence_length):
    """Đọc parallel_signal từ file .txt, xử lý dòng trống mạnh mẽ."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        parallel_signal = []
        current_user = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('parallel_signal='):
                numbers = [int(x) for x in line.split()]
                if len(numbers) == sequence_length:
                    current_user.append(numbers)
                if len(current_user) == K:
                    parallel_signal.append(current_user)
                    current_user = []

        if current_user and len(current_user) == K:
            parallel_signal.append(current_user)

        parallel_signal = np.array(parallel_signal)
        if parallel_signal.shape != (N, K, sequence_length):
            raise ValueError(f"Kích thước parallel_signal không khớp: kỳ vọng ({N}, {K}, {sequence_length}), nhận {parallel_signal.shape}")
        return parallel_signal
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file {input_file}")
    except Exception as e:
        raise Exception(f"Lỗi khi đọc parallel_signal từ {input_file}: {str(e)}")

# Hàm đọc thông số và gold_codes
def load_parameters(input_file):
    """Đọc thông số và gold_codes từ file .txt."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        N = None
        K = None
        sequence_length = 127
        gold_codes = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('N='):
                N = int(line.split('=')[1])
            elif line.startswith('K='):
                K = int(line.split('=')[1])
            elif line and not line.startswith('gold_codes='):
                gold_code = list(map(float, line.split()))
                gold_codes.append(gold_code)

        gold_codes = np.array(gold_codes)
        if N is None or K is None or sequence_length is None:
            raise ValueError("Thiếu thông số cần thiết trong file .txt")
        if gold_codes.shape != (N, sequence_length):
            raise ValueError(f"Kích thước gold_codes không khớp: kỳ vọng ({N}, {sequence_length})")

        return gold_codes, N, K, sequence_length
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file thông số {input_file}")
    except Exception as e:
        raise Exception(f"Lỗi khi đọc thông số: {str(e)}")

# Hàm nhân tín hiệu với PN sequence
def multiply_signal(parallel_signal, gold_codes, N, K, sequence_length):
    """Nhân tín hiệu parallel với Gold code."""
    multiplied_signal = np.zeros((N, K, sequence_length))
    for i in range(N):
        for k in range(K):
            multiplied_signal[i, k, :] = parallel_signal[i, k, :] * gold_codes[i, :]
    return multiplied_signal

# Hàm lưu multiplied_signal vào file .txt
def save_multiplied_signal(multiplied_signal, output_file='multiplied_output.txt'):
    """Lưu multiplied_signal vào file .txt."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("multiplied_signal=\n")
            for i in range(multiplied_signal.shape[0]):
                for k in range(multiplied_signal.shape[1]):
                    signal_str = ' '.join(map(str, multiplied_signal[i, k].astype(int)))
                    f.write(f"{signal_str}\n")
                f.write("\n")
        print(f"Đã lưu multiplied_signal tại: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Lỗi khi lưu multiplied_signal: {str(e)}")

# Hàm chính
def main():
    parser = argparse.ArgumentParser(description='Nhân tín hiệu với PN sequence.')
    parser.add_argument('-p','--parameters_file', type=str, required=True, help='Đường dẫn đến file parameters.txt')
    parser.add_argument('-pr','--parallel_file', type=str, required=True, help='Đường dẫn đến file parallel_output.txt')
    args = parser.parse_args()

    parameters_file = args.parameters_file
    parallel_file = args.parallel_file

    try:
        # Đọc thông số và gold_codes
        gold_codes, N, K, sequence_length = load_parameters(parameters_file)

        # Đọc parallel_signal
        parallel_signal = load_parallel_signal(parallel_file, N, K, sequence_length)

        # Nhân với PN sequence
        multiplied_signal = multiply_signal(parallel_signal, gold_codes, N, K, sequence_length)

        # Lưu kết quả
        save_multiplied_signal(multiplied_signal)

    except Exception as e:
        print(f"Lỗi khi chạy chương trình: {str(e)}")

if __name__ == "__main__":
    main()