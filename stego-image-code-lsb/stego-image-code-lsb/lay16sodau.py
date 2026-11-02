import sys

def extract_first_16_numbers(txt_path, output_txt_path):
    # Danh sách để lưu tất cả các số
    numbers = []
    
    # Đọc file graymatrix.txt
    with open(txt_path, 'r') as f:
        for line in f:
            # Tách các số trong dòng bằng dấu cách và chuyển thành int
            row_numbers = [int(num) for num in line.strip().split()]
            numbers.extend(row_numbers)
            # Dừng khi đã có ít nhất 16 số
            if len(numbers) >= 16:
                break
    
    # Lấy 16 số đầu tiên (hoặc ít hơn nếu file không đủ 16 số)
    first_16 = numbers[:16]
    
    # In kết quả
    print("16 so dau tien trong file graymatrix.txt:")
    print(first_16)
    
    # Lưu vào file 16sodau.txt
    with open(output_txt_path, 'w') as f:
        f.write(' '.join(map(str, first_16)))
    print(f"Da luu 16 so dau tien vao file {output_txt_path}")
    
    return first_16

# Sử dụng
extract_first_16_numbers(sys.argv[1], "16sodau.txt") 
# bien o day la file graymatrix.txt
