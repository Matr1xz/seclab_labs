import sys
def replace_first_16_numbers(input_matrix_path, input_16_path, output_matrix_path):
    # Đọc 16 số từ file 16sodausaugiau.txt
    with open(input_16_path, 'r') as f:
        new_16_numbers = [int(num) for num in f.read().strip().split()]
    if len(new_16_numbers) < 16:
        raise ValueError("File 16sodausaugiau.txt phai chua it nhat 16 so!")

    # Đọc ma trận từ graymatrix.txt vào danh sách 1D
    matrix_1d = []
    with open(input_matrix_path, 'r') as f:
        for line in f:
            row_numbers = [int(num) for num in line.strip().split()]
            matrix_1d.extend(row_numbers)
    
    # Kiểm tra xem ma trận có đủ 16 số không
    if len(matrix_1d) < 16:
        raise ValueError("File graymatrix.txt khong du 16 so de thay the!")
    
    # Thay 16 số đầu tiên
    matrix_1d[:16] = new_16_numbers[:16]
    
    # Đọc lại graymatrix.txt để lấy kích thước ma trận gốc
    with open(input_matrix_path, 'r') as f:
        lines = f.readlines()
        num_rows = len(lines)
        num_cols = len(lines[0].strip().split())
    
    # Chuyển mảng 1D về ma trận 2D
    new_matrix_2d = []
    index = 0
    for _ in range(num_rows):
        row = matrix_1d[index:index + num_cols]
        new_matrix_2d.append(row)
        index += num_cols
    
    # Lưu ma trận mới vào newgraymatrix.txt
    with open(output_matrix_path, 'w') as f:
        for row in new_matrix_2d:
            f.write(' '.join(map(str, row)) + '\n')
    print(f"Da luu ma tran anh vao {output_matrix_path}")

# Sử dụng
replace_first_16_numbers(sys.argv[1], sys.argv[2], "newgraymatrix.txt")
