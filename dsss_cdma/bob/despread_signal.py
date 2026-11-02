import numpy as np
import argparse
import os

# Hàm đọc multiplied_signal từ file .txt
def load_multiplied_signal(input_file, N, K, sequence_length):
    """Đọc multiplied_signal từ file .txt, xử lý dòng trống mạnh mẽ."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        multiplied_signal = []
        current_user = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('multiplied_signal='):
                numbers = [int(x) for x in line.split()]
                if len(numbers) == sequence_length:
                    current_user.append(numbers)
                if len(current_user) == K:
                    multiplied_signal.append(current_user)
                    current_user = []

        if current_user and len(current_user) == K:
            multiplied_signal.append(current_user)

        multiplied_signal = np.array(multiplied_signal)
        if multiplied_signal.shape != (N, K, sequence_length):
            raise ValueError(f"Kích thước multiplied_signal không khớp: kỳ vọng ({N}, {K}, {sequence_length}), nhận {multiplied_signal.shape}")
        return multiplied_signal
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file {input_file}")
    except Exception as e:
        raise Exception(f"Lỗi khi đọc multiplied_signal từ {input_file}: {str(e)}")

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

# Hàm giải trải phổ
def despread_signal(multiplied_signal, N, K, sequence_length):
    """Giải trải phổ bằng cách tích lũy kết quả nhân."""
    despreaded_data = np.zeros((N, K))
    for i in range(N):
        for k in range(K):
            despreaded_data[i, k] = np.sum(multiplied_signal[i, k, :]) / sequence_length
    return despreaded_data

# Hàm lưu despreaded_data vào file .txt
def save_despreaded_data(despreaded_data, output_file='despreaded_output.txt'):
    """Lưu despreaded_data vào file .txt."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("despreaded_data=\n")
            for i in range(despreaded_data.shape[0]):
                data_str = ' '.join(map(str, despreaded_data[i]))
                f.write(f"{data_str}\n")
        print(f"Đã lưu despreaded_data tại: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Lỗi khi lưu despreaded_data: {str(e)}")

# Hàm chính
def main():
    parser = argparse.ArgumentParser(description='Giải trải phổ tín hiệu.')
    parser.add_argument('-p','--parameters_file', type=str, required=True, help='Đường dẫn đến file parameters.txt')
    parser.add_argument('-m','--multiplied_file', type=str, required=True, help='Đường dẫn đến file multiplied_output.txt')
    args = parser.parse_args()

    parameters_file = args.parameters_file
    multiplied_file = args.multiplied_file

    try:
        # Đọc thông số
        N, K, sequence_length = load_parameters(parameters_file)

        # Đọc multiplied_signal
        multiplied_signal = load_multiplied_signal(multiplied_file, N, K, sequence_length)

        # Giải trải phổ
        despreaded_data = despread_signal(multiplied_signal, N, K, sequence_length)

        # Lưu kết quả
        save_despreaded_data(despreaded_data)

    except Exception as e:
        print(f"Lỗi khi chạy chương trình: {str(e)}")

if __name__ == "__main__":
    main()