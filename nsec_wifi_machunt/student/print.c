#include <stdio.h>

int main(){
	char input[100];
	printf("Enter target's name: ");
	fgets(input, sizeof(input), stdin);
	printf("%s", input);
	return 0;
}
