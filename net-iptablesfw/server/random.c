#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

int main() {
    // Đặt seed cho hàm ngẫu nhiên dựa trên thời gian hiện tại
    srand(time(NULL));

    // Mảng chứa các ký tự bạn muốn sử dụng để tạo chuỗi ngẫu nhiên
    char characters[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    int length = sizeof(characters) - 1; // Độ dài của mảng ký tự

    int string_length = 10; // Độ dài của chuỗi ngẫu nhiên bạn muốn tạo

    // Tạo chuỗi ngẫu nhiên
    char random_string[string_length + 1]; // +1 để chứa ký tự kết thúc chuỗi '\0'
    for (int i = 0; i < string_length; i++) {
        int random_index = rand() % length; // Chọn một ký tự ngẫu nhiên từ mảng characters
        random_string[i] = characters[random_index];
    }
    random_string[string_length] = '\0'; // Đảm bảo chuỗi kết thúc bằng '\0'

    // Chuỗi bạn muốn nối vào chuỗi ngẫu nhiên
    char additional_string[] = "Ptit ATTT ";

    // Tên tệp tin txt mà bạn muốn tạo hoặc ghi vào
    const char *file_name = "filerandom.txt";

    // Mở tệp tin để ghi (hoặc tạo tệp nếu chưa tồn tại)
    FILE *file = fopen(file_name, "w");
    if (file == NULL) {
        printf("Không thể mở tệp tin %s\n", file_name);
        return 1;
    }

    // In chuỗi vào tệp tin
    fprintf(file, "%s%s\n", additional_string, random_string);

    // Đóng tệp tin
    fclose(file);
    return 0;
}

