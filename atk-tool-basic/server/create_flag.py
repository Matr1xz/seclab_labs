# -*- coding: utf-8 -*-
import os
import random

def create_random_flag():
    # Các thư mục mục tiêu
    directories = ["/home/ubuntu/Security", "/home/ubuntu/AppData", "/home/ubuntu/Sharing"]
    
    # Tạo tất cả các thư mục nếu chưa tồn tại
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
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
        "SUCESS_29AQ39_WELL_DONE",
        "THANK_FOR_DOING_LABS_12HS643X"
    ]
    content = random.choice(content_choices)
    
    # Tạo file với nội dung
    f = open(file_path, "w")  # Mở file theo cách thủ công
    f.write(content)  # Ghi nội dung vào file
    f.close()  # Đóng file
    
    # Sử dụng print không dấu ngoặc trong Python 2
    print "Flag created at:", file_path, "with content:", content

# Chạy hàm
if __name__ == "__main__":
    create_random_flag()

