import numpy as np
import sys

path = sys.argv[1]
gray_array = np.loadtxt(path, dtype=np.float64)
height, width = gray_array.shape

pad_h = (8 - height % 8) % 80
pad_w = (8 - width % 8) % 8
gray_padded = np.pad(gray_array, ((0, pad_h), (0, pad_w)), mode='constant')
H, W = gray_padded.shape

num_blocks_h = H // 8
num_blocks_w = W // 8

while True:
    try:
        i_block = int(sys.argv[2])
        j_block = int(sys.argv[3])

        if 0 <= i_block < num_blocks_h and 0 <= j_block < num_blocks_w:
            break
        else:
            print("Vi tri khoi ma tran khong hop le.\n")
    except ValueError:
        print("Gia tri phai la so nguyen.\n")

start_row = i_block * 8
start_col = j_block * 8

gray_block_8x8 = gray_padded[start_row:start_row+8, start_col:start_col+8]

np.savetxt(f"extracted_matrix/matrix_8x8_vitri_{i_block}_{j_block}.txt", gray_block_8x8, fmt="%d")
print("Trich xuat thanh cong ma tran tai vi tri: ", i_block, ", ", j_block, sep="")

