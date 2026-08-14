import os
import random

def create_two_random_flags():
    directories = ["/home/ubuntu/Security", "/home/ubuntu/AppData", "/home/ubuntu/Sharing"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Chọn 2 thư mục KHÁC NHAU
    selected_dirs = random.sample(directories, 2)

    file_names = random.sample([
        "THIS_IS_FLAG5742AB2.txt",
        "CAPTURE_THE_FLAG03468DQ1.txt"
    ], 2)

    contents = random.sample([
        "U1VDRVNTXzI5QVEzOV9XRUxMX0RPTkU=",         # SUCCESS_29AQ39_WELL_DONE
        "VEhBTktfRk9SX0RPSU5HX0xBQlNfMTJIUzY0M1g="  # THANK_FOR_DOING_LABS_12HS643X
    ], 2)

    for i in range(2):
        file_path = os.path.join(selected_dirs[i], file_names[i])
        with open(file_path, "w") as f:
            f.write(contents[i])
        print(f"[{i+1}] Flag created at: {file_path} with content: {contents[i]}")

if __name__ == "__main__":
    create_two_random_flags()


