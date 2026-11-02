import numpy as np
import argparse
import os

# Hàm đọc demodulated_signal từ file .txt
def load_demodulated_signal(input_file):
    """Đọc demodulated_signal từ file .txt."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        demodulated_signal = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('demodulated_signal='):
                demodulated_signal.append([int(x) for x in line.split()])

        demodulated_signal = np.array(demodulated_signal)
        return demodulated_signal
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file {input_file}")
    except Exception as e:
        raise Exception(f"Lỗi khi đọc demodulated_signal từ {input_file}: {str(e)}")

# Hàm đọc thông số
def load_parameters(input_file):
    """Đọc thông số từ file .txt."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        N = None
        K = None
        sequence_length = 127
        
        for line in lines:
            line = line.strip()
            if line.startswith('N='):
                N = int(line.split('=')[1])
            elif line.startswith('K='):
                K = int(line.split('=')[1])

        if N is None or K is None or sequence_length is None:
            raise ValueError("Thiếu thông số cần thiết trong file .txt")

        return N, K, sequence_length
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file thông số {input_file}")
    except Exception as e:
        raise Exception(f"Lỗi khi đọc thông số: {str(e)}")

# Hàm chuyển đổi serial sang parallel
def serial_to_parallel(demodulated_signal, N, K, sequence_length):
    """Chuyển đổi tín hiệu serial thành vector parallel 127 mẫu."""
    parallel_signal = np.zeros((N, K, sequence_length))
    for i in range(N):
        for k in range(K):
            start_idx = k * sequence_length
            end_idx = start_idx + sequence_length
            if end_idx <= len(demodulated_signal[i]):
                parallel_signal[i, k, :] = demodulated_signal[i, start_idx:end_idx]
            else:
                parallel_signal[i, k, :] = 0
    return parallel_signal

# Hàm lưu parallel_signal vào file .txt
def save_parallel_signal(parallel_signal, output_file='parallel_output.txt'):
    """Lưu parallel_signal vào file .txt."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("parallel_signal=\n")
            for i in range(parallel_signal.shape[0]):
                for k in range(parallel_signal.shape[1]):
                    signal_str = ' '.join(map(str, parallel_signal[i, k].astype(int)))
                    f.write(f"{signal_str}\n")
                f.write("\n")
        print(f"Đã lưu parallel_signal tại: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Lỗi khi lưu parallel_signal: {str(e)}")

# Hàm chính
def main():
    parser = argparse.ArgumentParser(description='Chuyển đổi tín hiệu serial sang parallel.')
    parser.add_argument('-p','--parameters_file', type=str, required=True, help='Đường dẫn đến file parameters.txt')
    parser.add_argument('-df','--demodulated_file', type=str, required=True, help='Đường dẫn đến file demodulated_output.txt')
    args = parser.parse_args()

    parameters_file = args.parameters_file
    demodulated_file = args.demodulated_file

    try:
        # Đọc thông số
        N, K, sequence_length = load_parameters(parameters_file)

        # Đọc demodulated_signal
        demodulated_signal = load_demodulated_signal(demodulated_file)
        if demodulated_signal.shape[0] != N or demodulated_signal.shape[1] != K * sequence_length:
            raise ValueError(f"Kích thước demodulated_signal không khớp: kỳ vọng ({N}, {K*sequence_length})")

        # Chuyển đổi serial sang parallel
        parallel_signal = serial_to_parallel(demodulated_signal, N, K, sequence_length)

        # Lưu kết quả
        save_parallel_signal(parallel_signal)

    except Exception as e:
        print(f"Lỗi khi chạy chương trình: {str(e)}")

if __name__ == "__main__":
    main()