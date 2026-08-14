import os
import random

def create_random_flags():
    # Các thư mục mục tiêu
    directories = ["/home/ubuntu/Security", "/home/ubuntu/AppData", "/home/ubuntu/Sharing"]
    
    # Tạo tất cả các thư mục nếu chưa tồn tại
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Tên file và nội dung có thể
    file_name_choices = [
        "THIS_IS_FLAG5742AB2.txt",
        "CAPTURE_THE_FLAG03468DQ1.txt"
    ]
    
    content_choices = [
        "SUCESS_29AQ39_WELL_DONE",
        "THANK_FOR_DOING_LABS_12HS643X"
    ]

    # Shuffle để phân phối ngẫu nhiên
    random.shuffle(directories)
    random.shuffle(file_name_choices)
    random.shuffle(content_choices)

    # Tạo 2 file
    for i in range(2):
        target_dir = random.choice(directories)
        file_name = file_name_choices[i]
        content = content_choices[i]
        file_path = os.path.join(target_dir, file_name)

        with open(file_path, "w") as f:
            f.write(content)

        print(f"Flag {i+1} created at: {file_path} with content: {content}")

if __name__ == "__main__":
    create_random_flags()

