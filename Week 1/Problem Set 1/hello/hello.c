#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Ask user for name
    string name = get_string("What is your name? ");

    //Greet user
    printf("hello, %s\n", name);
}