import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from scipy.io import wavfile
import argparse

# Hàm đọc spreaded_signal từ file .txt
def load_spread_output(input_file):
    """Đọc spreaded_signal từ file .txt."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        spreaded_signal = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('spreaded_signal='):
                spreaded_signal.append([int(x) for x in line.split()])

        spreaded_signal = np.array(spreaded_signal)
        return spreaded_signal
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file {input_file}")
    except Exception as e:
        raise Exception(f"Lỗi khi đọc spreaded_signal từ {input_file}: {str(e)}")

# Hàm đọc K từ file bpsk_output.txt
def load_K(input_file):
    """Đọc K từ file bpsk_output.txt."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        K = None
        for line in lines:
            line = line.strip()
            if line.startswith('K='):
                K = int(line.split('=')[1])
                break
        if K is None:
            raise ValueError(f"Không tìm thấy K trong file {input_file}")
        return K
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file {input_file}")
    except Exception as e:
        raise Exception(f"Lỗi khi đọc K từ {input_file}: {str(e)}")

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

# Hàm nhúng tín hiệu vào file âm thanh
def embed_signal_to_audio(spreaded_signal, N, K, sequence_length, input_audio_path, output_audio_path, amplitude=0.01):
    """Nhúng tín hiệu trải phổ vào file âm thanh."""
    try:
        sample_rate, audio_data = wavfile.read(input_audio_path)
        is_stereo = len(audio_data.shape) > 1
        num_channels = audio_data.shape[1] if is_stereo else 1
        dtype = audio_data.dtype

        total_signal = np.sum(spreaded_signal, axis=0)
        signal_length = K * sequence_length
        audio_length = audio_data.shape[0]
        if signal_length > audio_length:
            print(f"Cảnh báo: Tín hiệu dài hơn âm thanh ({signal_length} > {audio_length}). Cắt bớt tín hiệu.")
            total_signal = total_signal[:audio_length]
        else:
            repeat_times = int(np.ceil(audio_length / signal_length))
            total_signal = np.tile(total_signal, repeat_times)[:audio_length]

        audio_data = audio_data.astype(np.float32)
        max_audio = np.max(np.abs(audio_data))
        if max_audio > 0:
            audio_data = audio_data / max_audio

        embedded_audio = np.copy(audio_data)
        if is_stereo:
            for channel in range(num_channels):
                embedded_audio[:, channel] += amplitude * total_signal
        else:
            embedded_audio += amplitude * total_signal

        max_embedded = np.max(np.abs(embedded_audio))
        if max_embedded > 0:
            embedded_audio = embedded_audio / max_embedded * max_audio

        embedded_audio = np.clip(embedded_audio, np.iinfo(dtype).min, np.iinfo(dtype).max).astype(dtype)
        wavfile.write(output_audio_path, sample_rate, embedded_audio)
        print(f"Đã lưu file âm thanh chứa thông điệp tại: {os.path.abspath(output_audio_path)}")
        return total_signal

    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file âm thanh {input_audio_path}")
    except Exception as e:
        raise Exception(f"Lỗi khi nhúng tín hiệu vào âm thanh: {str(e)}")

# Hàm lưu total_signal vào file .txt
def save_total_signal(total_signal, output_file='total_signal_output.txt'):
    """Lưu total_signal vào file .txt."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            total_signal_str = ' '.join(map(str, total_signal.astype(float)))
            f.write(f"total_signal=\n{total_signal_str}\n")
        print(f"Đã lưu total_signal tại: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Lỗi khi lưu total_signal: {str(e)}")

# Hàm lưu thông số
def save_parameters(gold_codes, N, K, output_file='parameters.txt'):
    """Lưu thông số cần thiết cho giải tín hiệu vào file .txt."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"N={N}\n")
            f.write(f"K={K}\n")
            f.write("gold_codes=\n")
            for i in range(N):
                gold_code_str = ' '.join(map(str, gold_codes[i].astype(int)))
                f.write(f"{gold_code_str}\n")
        print(f"Đã lưu thông số tại: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Lỗi khi lưu thông số: {str(e)}")

# Hàm vẽ biểu đồ tín hiệu nhúng
def plot_embedded_signal(total_signal, sequence_length):
    """Vẽ biểu đồ tín hiệu nhúng."""
    plt.figure(figsize=(10, 4))
    samples_to_plot = min(1000, len(total_signal))
    plt.plot(total_signal[:samples_to_plot], label='Tín hiệu nhúng')
    plt.title('Tín hiệu trải phổ nhúng trong âm thanh')
    plt.xlabel('Mẫu')
    plt.ylabel('Biên độ')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    output_file = 'embedded_signal.png'
    plt.savefig(output_file)
    print(f"Biểu đồ tín hiệu nhúng đã được lưu tại: {os.path.abspath(output_file)}")
    plt.close()

# Hàm chính
def main():
    # Thiết lập parser để nhận tham số dòng lệnh
    parser = argparse.ArgumentParser(description='Nhúng tín hiệu vào âm thanh và vẽ biểu đồ.')
    parser.add_argument('-n', '--N', type=int, required=True, help='Số lượng người dùng')
    parser.add_argument('-i', '--input_audio_path', type=str, required=True, help='Đường dẫn file âm thanh đầu vào')
    parser.add_argument('-b', '--bpsk_file', type=str, required=True, help='Đường dẫn đến file bpsk_output.txt')
    parser.add_argument('-g', '--gold_codes_file', type=str, required=True, help='Đường dẫn đến file gold_codes_output.txt')
    parser.add_argument('-s', '--spread_file', type=str, required=True, help='Đường dẫn đến file spread_output.txt')
    args = parser.parse_args()

    N = args.N
    input_audio_path = args.input_audio_path
    bpsk_file = args.bpsk_file
    gold_codes_file = args.gold_codes_file
    spread_file = args.spread_file
    output_audio_path = 'output_with_message.wav'
    sequence_length = 127
    amplitude = 0.01

    try:
        # Đọc K từ bpsk_output.txt
        K = load_K(bpsk_file)

        # Đọc spreaded_signal từ spread_output.txt
        spreaded_signal = load_spread_output(spread_file)
        if spreaded_signal.shape[0] != N or spreaded_signal.shape[1] != K * sequence_length:
            raise ValueError(f"Kích thước spreaded_signal không khớp: kỳ vọng ({N}, {K*sequence_length})")

        # Đọc gold_codes từ gold_codes_output.txt
        gold_codes = load_gold_codes(gold_codes_file)
        if gold_codes.shape[0] != N or gold_codes.shape[1] != sequence_length:
            raise ValueError(f"Kích thước gold_codes không khớp: kỳ vọng ({N}, {sequence_length})")

        # Nhúng tín hiệu vào âm thanh
        total_signal = embed_signal_to_audio(spreaded_signal, N, K, sequence_length, input_audio_path, output_audio_path, amplitude)

        # Lưu total_signal
        save_total_signal(total_signal)

        # Lưu thông số
        save_parameters(gold_codes, N, K)

        # Vẽ biểu đồ
        plot_embedded_signal(total_signal, sequence_length)

    except Exception as e:
        print(f"Lỗi khi chạy chương trình: {str(e)}")

if __name__ == "__main__":
    main()
