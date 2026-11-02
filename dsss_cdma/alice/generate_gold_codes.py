import numpy as np
import argparse
import os

# Hàm tạo trạng thái ban đầu cho LFSR
def generate_lfsr_state(shift_value, degree):
    """Tạo trạng thái ban đầu không bằng 0 cho LFSR dựa trên giá trị dịch."""
    if shift_value <= 0:
        state = [0] * (degree - 1) + [1]
    else:
        state_str = bin(shift_value)[2:].zfill(degree)
        state = [int(b) for b in state_str[-degree:]]

    if all(s == 0 for s in state):
        state = [0] * (degree - 1) + [1]
    return state

# Hàm tạo chuỗi PN bằng LFSR Fibonacci
def generate_pn_sequence_fibonacci(gen_poly_powers, initial_shift, num_bits):
    """Tạo chuỗi PN bằng LFSR Fibonacci."""
    if not gen_poly_powers or gen_poly_powers[-1] != 0:
        raise ValueError("Đa thức sinh yêu cầu bậc thấp nhất (bậc 0). Ví dụ: [3, 2, 0]")

    degree = gen_poly_powers[0]
    tap_powers = [p for p in gen_poly_powers if p != degree]

    state = generate_lfsr_state(initial_shift, degree)
    sequence = []
    current_state = list(state)

    for _ in range(num_bits):
        output_bit = current_state[-1]
        sequence.append(output_bit)

        feedback_bit = 0
        for p in tap_powers:
            tap_index = degree - 1 - p
            if 0 <= tap_index < degree:
                feedback_bit ^= current_state[tap_index]

        current_state.pop()
        current_state.insert(0, feedback_bit)

    return np.array(sequence)

# Hàm tạo Gold codes
def generate_gold_codes(N, sequence_length=127):
    """Tạo Gold codes cho N người dùng bằng hai LFSRs 7 bit."""
    degree = 7
    gen_poly1 = [7, 3, 0]  # x^7 + x^3 + 1
    gen_poly2 = [7, 3, 2, 1, 0]  # x^7 + x^3 + x^2 + x + 1

    gold_codes = np.zeros((N, sequence_length))
    for i in range(N):
        shift = i + 1
        seq1 = generate_pn_sequence_fibonacci(gen_poly1, shift, sequence_length)
        seq2 = generate_pn_sequence_fibonacci(gen_poly2, shift, sequence_length)
        gold_code = np.logical_xor(seq1, seq2).astype(int)
        gold_codes[i, :] = gold_code
        gold_codes[i, gold_codes[i, :] == 0] = -1
    return gold_codes

# Hàm lưu gold_codes vào file .txt
def save_gold_codes(gold_codes, output_file='gold_codes_output.txt'):
    """Lưu gold_codes vào file .txt."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("gold_codes=\n")
            for i in range(gold_codes.shape[0]):
                gold_code_str = ' '.join(map(str, gold_codes[i].astype(int)))
                f.write(f"{gold_code_str}\n")
        print(f"Đã lưu gold_codes tại: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Lỗi khi lưu gold_codes: {str(e)}")

# Hàm chính
def main():
    # Thiết lập parser để nhận tham số dòng lệnh
    parser = argparse.ArgumentParser(description='Tạo Gold codes.')
    parser.add_argument('-n','--N', type=int, required=True, help='Số lượng người dùng')
    args = parser.parse_args()

    N = args.N
    sequence_length = 127

    try:
        # Tạo Gold codes
        gold_codes = generate_gold_codes(N, sequence_length)
        print(gold_codes)
        # Lưu kết quả
        save_gold_codes(gold_codes)

    except Exception as e:
        print(f"Lỗi khi chạy chương trình: {str(e)}")

if __name__ == "__main__":
    main()
