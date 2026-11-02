import numpy as np
import sys

Q_Y = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])

def quantize_dct(dct_matrix, quantization_matrix):
    return np.round(dct_matrix / quantization_matrix).astype(int)

def apply_quantization_to_single_matrix(input_file, output_file):

    dct_matrix = np.loadtxt(input_file, dtype=np.float64)

    quantized_matrix = quantize_dct(dct_matrix, Q_Y)

    np.savetxt(output_file, quantized_matrix, fmt="%d")

    print(f"Da luong tu hoa: '{output_file}'.")

input_file = sys.argv[1]
output_file = input_file

apply_quantization_to_single_matrix(input_file, output_file)
