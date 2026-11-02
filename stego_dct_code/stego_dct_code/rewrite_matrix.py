import numpy as np
import sys

path1 = sys.argv[1]
gray_array = np.loadtxt(path1, dtype=np.float64)
height, width = gray_array.shape

pad_h = (8 - height % 8) % 8
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
        
path2 = sys.argv[4]
idct_block = np.loadtxt(path2, dtype=np.float64)

if idct_block.shape != (8, 8):
    raise ValueError("Loi ma tran.")

start_row = i_block * 8
start_col = j_block * 8
gray_padded[start_row:start_row+8, start_col:start_col+8] = idct_block

gray_array_output = gray_padded[:height, :width]

np.savetxt("image_matrix.txt", gray_array_output, fmt="%d")
print("Da thay the thanh cong khoi ma tran trong: 'image_matrix.txt'")
