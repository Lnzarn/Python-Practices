#include <stdio.h>

int main() {
    int arr[3][3] = {{1,2,3}, {4,9,6}, {10,8,5}};

    int max = arr[0][0];
    int ypos = 0;
    int xpos = 0;
    for(int i = 0; i < 3; i++) {
        for(int j = 0; j < 3; j++) {
            if (max < arr[i][j]) {
                max = arr[i][j];
                ypos = i;
                xpos = j;
            }
        }
    }

    printf("\n The max is %d at [%d][%d]", max, ypos, xpos);
}