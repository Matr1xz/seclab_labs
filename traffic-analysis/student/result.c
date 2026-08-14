#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *file;
    char filename[100];
    char ch;
    printf("Enter the name of the file to read: ");
    scanf("%s", filename);
    file = fopen(filename, "r");
    if (file == NULL) {
        printf("Could not open file %s\n", filename);
        return 1;
    }
    while ((ch = fgetc(file)) != EOF) {
        putchar(ch);
    }
    fclose(file);

    return 0;
}

