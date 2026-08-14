import os
import random

def create_random_flags():
    # Các thư mục mục tiêu
    directories = ["/home/ubuntu/Security", "/home/ubuntu/AppData", "/home/ubuntu/Sharing"]

    # Tạo tất cả các thư mục nếu chưa tồn tại
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Danh sách tên file và nội dung
    file_name_choices = [
        "THIS_IS_FLAG5742AB2.txt",
        "CAPTURE_THE_FLAG03468DQ1.txt"
    ]

    content_choices = [
        "SUCESS_29AQ39_WELL_DONE",
        "THANK_FOR_DOING_LABS_12HS643X"
    ]

    # Shuffle để ngẫu nhiên hoá phân phối
    random.shuffle(file_name_choices)
    random.shuffle(content_choices)

    # Tạo 2 file với nội dung khác nhau
    for i in range(2):
        file_name = file_name_choices[i]
        content = content_choices[i]
        target_dir = random.choice(directories)  # có thể trùng nhau

        file_path = os.path.join(target_dir, file_name)

        with open(file_path, "w") as f:
            f.write(content)

        print(f"[+] Flag {i+1} created at: {file_path}")
        print(f"    └── Content: {content}")

if __name__ == "__main__":
    create_random_flags()

