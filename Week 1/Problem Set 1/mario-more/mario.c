#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        //Ask user for number representing height of the pyramid
        n = get_int("Height: ");
    }
    //Ask user until number between 1 and 8 inclusive provided
    while (n < 1 || n > 8);

    //For loop that keeps track of the pyramid's height
    for (int i = 0; i < n; i++)
    {
        //Print spaces on the left side
        for (int k = 2; k <= n - i; k++)
        {
            printf(" ");
        }

        //Print left pyramid
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        //Print gap between pyramids
        printf("  ");

        //Print right pyramid
        for (int l = 0; l <= i; l++)
        {
            printf("#");
        }

        printf("\n");
    }
}