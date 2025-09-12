#include <stdio.h>
#include <conio.h>

int divisibleBy3(int rows, int column, int arr[rows][column]);

// int validateInput(char *prompt, int *input);
int validateValue(int rows, int column);

int main()
{

  int rows = 3, column = 3;
  int again = 0;
  do {
    // validateInput("Enter the row:", &rows);
    // validateInput("Enter the column:", &column);

    int size = rows * column;
    int arr[rows][column];

    for (int i = 0; i < rows; i++)
    {
      for (int j = 0; j < column; j++)
      {
        arr[i][j] = validateValue(i, j);
      }
    }
    printf("\nThe Array:\n");
    for (int i = 0; i < rows; i++)
    {
      for (int j = 0; j < column; j++)
      {
        printf("%d\t", arr[i][j]);
      }
      printf("\n");
    }

    printf("\nThe Elements Divisible by 3:\n");
    divisibleBy3(rows, column, arr);

    printf("\nWould you like to try again? (1 for yes and 0 for no)\n>");
    scanf("%d", &again);
  } while (again == 1);
  
  return 0;
}

int divisibleBy3(int rows, int column, int arr[rows][column])
{
  for (int i = 0; i < rows; i++)
  {
    for (int j = 0; j < column; j++)
    {
      if (arr[i][j] % 3 == 0)
      {
        printf("%d, [%d] [%d] \n", arr[i][j], i, j);
      }
    }
  }
}

// int validateInput(char *prompt, int *input)
// {
//   int validInput;
//   do
//   {
//     printf("%s\t", prompt);
//     validInput = scanf("%d", input);

//     if (!validInput || *input < 1) {
//       printf("Enter a valid number.\n");
//       getchar();
//     }
//   } while (!validInput || *input < 1);
// }

int validateValue(int rows, int column) {
  int temp;
  while(1) {
    printf("Enter value of [%d][%d]:\t", rows, column);
    if (scanf("%d", &temp) == 1){
      return temp;
    } else {
      printf("\nPlease input the appropriate number:\n");
      getchar();
    }
  }
}