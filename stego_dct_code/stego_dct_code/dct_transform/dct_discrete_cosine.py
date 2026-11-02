import numpy as np
import sys

def dct_2d(matrix):
    T = np.array([
        [0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536],
        [0.4904, 0.4157, 0.2778, 0.0975, -0.0975, -0.2778, -0.4157, -0.4904],
        [0.4619, 0.1913, -0.1913, -0.4619, -0.4619, -0.1913, 0.1913, 0.4619],
        [0.4157, -0.0975, -0.4904, -0.2778, 0.2778, 0.4904, 0.0975, -0.4157],
        [0.3536, -0.3536, -0.3536, 0.3536, 0.3536, -0.3536, -0.3536, 0.3536],
        [0.2778, -0.4904, 0.0975, 0.4157, -0.4157, -0.0975, 0.4904, -0.2778],
        [0.1913, -0.4619, 0.4619, -0.1913, -0.1913, 0.4619, -0.4619, 0.1913],
        [0.0975, -0.2778, 0.4157, -0.4904, 0.4904, -0.4157, 0.2778, -0.0975]
    ])

    T_T = T.T

    D = np.dot(np.dot(T, matrix), T_T)

    return D

def apply_dct_to_single_matrix(input_file, output_file):

    matrix = np.loadtxt(input_file, dtype=np.float64)

    matrix_subtracted = matrix - 128

    dct_matrix = dct_2d(matrix_subtracted)

    np.savetxt(output_file, dct_matrix, fmt="%.4f")

    print(f"Da bien doi DCT: '{output_file}'.")

input_file = sys.argv[1]
output_file = input_file

apply_dct_to_single_matrix(input_file, output_file)
