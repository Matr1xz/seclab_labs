# -*-coding: utf-8 -*-
import os
import random

def create_random_flags():
    # Các thư mục mục tiêu
    directories = ["/home/ubuntu/Security", "/home/ubuntu/AppData", "/home/ubuntu/Sharing"]
    
    # Tạo thư mục nếu chưa có
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Chọn 2 thư mục KHÁC NHAU để đặt cờ
    target_dirs = random.sample(directories, 2)

    # Danh sách tên file và nội dung (đảm bảo không trùng nhau)
    file_name_choices = random.sample([
        "THIS_IS_FLAG5742AB2.txt",
        "CAPTURE_THE_FLAG03468DQ1.txt"
    ], 2)

    content_choices = random.sample([
        "SUCESS_29AQ39_WELL_DONE",
        "THANK_FOR_DOING_LABS_12HS643X"
    ], 2)

    # Tạo 2 flag ở 2 thư mục khác nhau
    for i in range(2):
        target_dir = target_dirs[i]
        file_name = file_name_choices[i]
        content = content_choices[i]
        file_path = os.path.join(target_dir, file_name)
        
        with open(file_path, "w") as f:
            f.write(content)
        
        print(f"[{i+1}] Flag created at: {file_path} with content: {content}")

# Chạy hàm
if __name__ == "__main__":
    create_random_flags()
