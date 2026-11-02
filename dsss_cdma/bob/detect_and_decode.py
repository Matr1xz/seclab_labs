import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import os

# Hàm đọc despreaded_data từ file .txt
def load_despreaded_data(input_file, N, K):
    """Đọc despreaded_data từ file .txt, xử lý dòng trống mạnh mẽ."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        despreaded_data = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('despreaded_data='):
                numbers = [float(x) for x in line.split()]
                if len(numbers) == K:
                    despreaded_data.append(numbers)

        despreaded_data = np.array(despreaded_data)
        if despreaded_data.shape != (N, K):
            raise ValueError(f"Kích thước despreaded_data không khớp: kỳ vọng ({N}, {K}), nhận {despreaded_data.shape}")
        return despreaded_data
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file {input_file}")
    except Exception as e:
        raise Exception(f"Lỗi khi đọc despreaded_data từ {input_file}: {str(e)}")

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

# Hàm phát hiện ngưỡng
def threshold_detector(despreaded_data, N, K, threshold=0.5):
    """Phát hiện bit dựa trên ngưỡng."""
    detected_data = np.zeros((N, K))
    for i in range(N):
        detected_data[i, :] = np.where(despreaded_data[i, :] >= threshold, 1, -1)
    return detected_data

# Hàm chuyển thông điệp về văn bản
def decode_to_text(detected_data, N, K):
    """Chuyển thông điệp ước lượng từ BPSK symbols về văn bản."""
    text_messages = []
    for i in range(N):
        bits = (detected_data[i, :] + 1) // 2
        text = ""
        for j in range(0, len(bits), 8):
            byte = bits[j:j+8]
            if len(byte) == 8:
                byte_str = ''.join(str(int(b)) for b in byte)
                char_code = int(byte_str, 2)
                if 32 <= char_code <= 126:
                    text += chr(char_code)
                else:
                    text += '?'
        text_messages.append(text)
    return text_messages

# Hàm lưu thông điệp giải trải phổ
def save_despreaded_message(despreaded_data, N, K):
    """Lưu thông điệp giải trải phổ vào file .txt."""
    for i in range(N):
        output_file = f'despreaded_user{i+1}.txt'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Thông điệp giải trải phổ cho người dùng {i+1}\n")
                f.write(str(despreaded_data[i, :]) + "\n")
            print(f"Đã lưu thông điệp giải trải phổ cho người dùng {i+1} vào: {os.path.abspath(output_file)}")
        except Exception as e:
            print(f"Lỗi khi lưu file {output_file}: {str(e)}")

# Hàm lưu thông điệp văn bản
def save_decoded_text(text_messages, N):
    """Lưu thông điệp văn bản vào file .txt."""
    for i in range(N):
        output_file = f'decoded_user{i+1}.txt'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Thông điệp văn bản giải mã cho người dùng {i+1}\n")
                f.write(text_messages[i] + "\n")
            print(f"Đã lưu thông điệp văn bản cho người dùng {i+1} vào: {os.path.abspath(output_file)}")
        except Exception as e:
            print(f"Lỗi khi lưu file {output_file}: {str(e)}")

# Hàm vẽ biểu đồ
def plot_results(despreaded_data, detected_data, N, K, sequence_length):
    """Vẽ biểu đồ so sánh tín hiệu giải trải phổ và ước lượng."""
    plt.figure(figsize=(10, 2 * N))
    for i in range(N):
        plt.subplot(N, 1, i + 1)
        x_axis = np.arange(min(K, 10))
        plt.step(x_axis, despreaded_data[i, :min(K, 10)], '-*', where='post', label='Sau giải trải phổ')
        plt.step(x_axis, detected_data[i, :min(K, 10)], '-x', where='post', label='Ước lượng')
        plt.ylim([-2, 2])
        plt.title(f'Người dùng {i+1}: Giải trải phổ vs Ước lượng (Gold code length: {sequence_length})')
        plt.xlabel("Chỉ số bit")
        plt.ylabel("Biên độ / Giá trị")
        plt.grid(True)
        plt.legend()
    plt.tight_layout()
    output_file = 'cdma_bpsk_results.png'
    plt.savefig(output_file)
    print(f"Biểu đồ kết quả đã được lưu tại: {os.path.abspath(output_file)}")
    plt.close()

# Hàm lưu detected_data vào file .txt
def save_detected_data(detected_data, output_file='detected_output.txt'):
    """Lưu detected_data vào file .txt."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("detected_data=\n")
            for i in range(detected_data.shape[0]):
                data_str = ' '.join(map(str, detected_data[i].astype(int)))
                f.write(f"{data_str}\n")
        print(f"Đã lưu detected_data tại: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Lỗi khi lưu detected_data: {str(e)}")

# Hàm chính
def main():
    parser = argparse.ArgumentParser(description='Phát hiện ngưỡng, giải mã và vẽ biểu đồ.')
    parser.add_argument('-p','--parameters_file', type=str, required=True, help='Đường dẫn đến file parameters.txt')
    parser.add_argument('-df','--despreaded_file', type=str, required=True, help='Đường dẫn đến file despreaded_output.txt')
    args = parser.parse_args()

    parameters_file = args.parameters_file
    despreaded_file = args.despreaded_file

    try:
        # Đọc thông số
        N, K, sequence_length = load_parameters(parameters_file)

        # Đọc despreaded_data
        despreaded_data = load_despreaded_data(despreaded_file, N, K)

        # Phát hiện ngưỡng
        detected_data = threshold_detector(despreaded_data, N, K)

        # Lưu detected_data
        save_detected_data(detected_data)

        # Lưu thông điệp giải trải phổ
        save_despreaded_message(despreaded_data, N, K)

        # Chuyển thông điệp về văn bản
        text_messages = decode_to_text(detected_data, N, K)
        print("Thông điệp văn bản giải mã:", text_messages)

        # Lưu thông điệp văn bản
        save_decoded_text(text_messages, N)

        # Vẽ biểu đồ
        plot_results(despreaded_data, detected_data, N, K, sequence_length)

    except Exception as e:
        print(f"Lỗi khi chạy chương trình: {str(e)}")

if __name__ == "__main__":
    main()