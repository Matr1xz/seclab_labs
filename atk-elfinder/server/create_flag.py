import os
import random

def create_random_flag():
    # Các thư mục mục tiêu
    directories = ["/home/ubuntu/Security", "/home/ubuntu/AppData", "/home/ubuntu/Sharing"]
    
    # Tạo tất cả các thư mục nếu chưa tồn tại
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Chọn ngẫu nhiên một thư mục để đặt cờ
    target_dir = random.choice(directories)
    
    # Chọn tên file ngẫu nhiên
    file_name_choices = [
        "THIS_IS_FLAG5742AB2.txt",
        "CAPTURE_THE_FLAG03468DQ1.txt"
    ]
    file_name = random.choice(file_name_choices)
    file_path = os.path.join(target_dir, file_name)
    
    # Nội dung ngẫu nhiên
    content_choices = [
        "U1VDRVNTXzI5QVEzOV9XRUxMX0RPTkU=",
        "VEhBTktfRk9SX0RPSU5HX0xBQlNfMTJIUzY0M1g="
    ]
    content = random.choice(content_choices)
    
    # Tạo file với nội dung
    with open(file_path, "w") as f:
        f.write(content)
    
    print(f"Flag created at: {file_path} with content: {content}")

# Chạy hàm
if __name__ == "__main__":
    create_random_flag()

