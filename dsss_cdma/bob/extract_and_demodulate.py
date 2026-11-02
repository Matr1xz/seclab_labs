import numpy as np
import argparse
import os
from scipy.io import wavfile

# Hàm đọc thông số
def load_parameters(input_file):
    """Đọc thông số từ file .txt."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        N = None
        K = None
        sequence_length = 127
        amplitude = 0.01
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
        if N is None or K is None or sequence_length is None or amplitude is None:
            raise ValueError("Thiếu thông số cần thiết trong file .txt")
        if gold_codes.shape != (N, sequence_length):
            raise ValueError(f"Kích thước gold_codes không khớp: kỳ vọng ({N}, {sequence_length}), nhận {gold_codes.shape}")

        return gold_codes, N, K, sequence_length, amplitude
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file thông số {input_file}")
    except Exception as e:
        raise Exception(f"Lỗi khi đọc thông số: {str(e)}")

# Hàm trích xuất tín hiệu từ file âm thanh
def extract_signal_from_audio(audio_path, K, sequence_length, amplitude):
    """Trích xuất tín hiệu trải phổ từ file âm thanh."""
    try:
        sample_rate, audio_data = wavfile.read(audio_path)
        is_stereo = len(audio_data.shape) > 1
        num_channels = audio_data.shape[1] if is_stereo else 1

        audio_data = audio_data.astype(np.float32)
        max_audio = np.max(np.abs(audio_data))
        if max_audio > 0:
            audio_data = audio_data / max_audio

        signal_length = K * sequence_length
        audio_length = audio_data.shape[0]
        if signal_length > audio_length:
            print(f"Cảnh báo: Độ dài tín hiệu ({signal_length}) lớn hơn âm thanh ({audio_length}). Cắt bớt.")
            audio_data = audio_data[:signal_length]
        else:
            audio_data = audio_data[:signal_length]

        if is_stereo:
            extracted_signal = np.mean(audio_data, axis=1)
        else:
            extracted_signal = audio_data

        extracted_signal = extracted_signal / amplitude
        return extracted_signal
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file âm thanh {audio_path}")
    except Exception as e:
        raise Exception(f"Lỗi khi trích xuất tín hiệu từ âm thanh: {str(e)}")

# Hàm mô phỏng BPSK demodulator
def bpsk_demodulate(received_signal, N, total_length):
    """Mô phỏng BPSK demodulator, tạo đầu ra 15 mức (-7 đến 7)."""
    demodulated_signal = received_signal + np.random.normal(0, 0.1, received_signal.shape)
    demodulated_signal = np.clip(demodulated_signal * 7, -7, 7)
    demodulated_signal = np.round(demodulated_signal).astype(int)
    return demodulated_signal

# Hàm lưu demodulated_signal vào file .txt
def save_demodulated_signal(demodulated_signal, output_file='demodulated_output.txt'):
    """Lưu demodulated_signal vào file .txt."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("demodulated_signal=\n")
            for i in range(demodulated_signal.shape[0]):
                signal_str = ' '.join(map(str, demodulated_signal[i].astype(int)))
                f.write(f"{signal_str}\n")
        print(f"Đã lưu demodulated_signal tại: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Lỗi khi lưu demodulated_signal: {str(e)}")

# Hàm chính
def main():
    parser = argparse.ArgumentParser(description='Trích xuất và demodulate tín hiệu từ âm thanh.')
    parser.add_argument('-p','--parameters_file', type=str, required=True, help='Đường dẫn đến file parameters.txt')
    parser.add_argument('-i','--audio_path', type=str, required=True, help='Đường dẫn đến file output_with_message.wav')
    args = parser.parse_args()

    parameters_file = args.parameters_file
    audio_path = args.audio_path

    try:
        # 1) Đọc thông số
        gold_codes, N, K, sequence_length, amplitude = load_parameters(parameters_file)
        print(f"Thông số: N={N}, K={K}, sequence_length={sequence_length}")

        # 2) Trích xuất tín hiệu từ âm thanh
        extracted_signal = extract_signal_from_audio(audio_path, K, sequence_length, amplitude)

        # 3) Tạo tín hiệu nhận được cho từng người dùng
        received_signal = np.tile(extracted_signal, (N, 1))

        # 4) BPSK demodulation
        demodulated_signal = bpsk_demodulate(received_signal, N, K * sequence_length)

        # Lưu kết quả
        save_demodulated_signal(demodulated_signal)

    except Exception as e:
        print(f"Lỗi khi chạy chương trình: {str(e)}")

if __name__ == "__main__":
    main()