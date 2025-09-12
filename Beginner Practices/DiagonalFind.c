#include <stdio.h>

int main() {
    int arr[4][4] = {{1,2,3,4}, {4,5,6,7}, {7,8,9,10}, {11, 12, 13,14}};
    printf("Array\n");
    for(int i = 0; i < 4; i++) {
        for(int j = 0; j < 4; j++) {
            printf("%d\t", arr[i][j]);
        }
        printf("\n");
    }
    printf("\n");
    for(int i = 0; i < 4; i++) {
        printf("%d\t", arr[i][i]);
    }

    printf("\n");
    for(int i = 0; i < 4; i++) {
        printf("%d\t", arr[i][3 - i]);
    }
    int find;
    int found = 0;
    printf("\n\nEnter:");
    scanf("%d", &find);

    for(int i = 0; i < 4; i++) {
        if (arr[i][3 - i]==find) {
            found = 1;
            printf("It is found in [%d][%d]", i, 3 - i);
        }   
    }
        
    if(!found) {
        printf("\n Not found in diagonals");
    }
}