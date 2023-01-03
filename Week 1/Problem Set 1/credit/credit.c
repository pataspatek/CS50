#include <cs50.h>
#include <stdio.h>

int first_part(long number);
int second_part(long number);
int first_digit(long number);
int second_digit(long number);
string check(int first, int second, long number, int lenght);
int lenght(long number);


int main(void)
{
    //Ask user for credit card number
    long card_number = get_long("Number: ");

    //Adds needed math together into checksum
    int checksum = first_part(card_number) + second_part(card_number);

    //Checks for valid checksum
    if (checksum % 10 == 0)
    {
        string company = check(first_digit(card_number), second_digit(card_number), card_number, lenght(card_number));
        printf("%s", company);
    }
    else
    {
        printf("INVALID\n");
    }
}


//First part of the checksum
int first_part(long number)
{
    int x, y, sum = 0;
    //Start with dividing the number by 10 to get rid of tle last digit
    number /= 10;
    for (int i = 0; i < 8; i++)
    {
        x = number % 10;
        x *= 2;
        if (x >= 10)
        {
            y = x % 10;
            y += 1;
            sum += y;
        }
        else
        {
            sum += x;
        }
        //Dividing by 100 steps to every other digit in a number
        number /= 100;
    }
    return sum;
}


//second part of the checksum
int second_part(long number)
{
    int x, sum = 0;
    for (int i = 0; i < 8; i++)
    {
        x = number % 10;
        sum += x;
        number /= 100;
    }
    return sum;
}


//Returned number is the first digit of the card number
int first_digit(long number)
{
    //Get one digit number
    while (number >= 10)
    {
        number /= 10;
    }
    return number;
}


//Returned number is the second digit of the card number
int second_digit(long number)
{
    //Get two digit number
    while (number >= 100)
    {
        number /= 10;
    }
    number %= 10;
    return number;
}


//Checks which company's card is given
string check(int first, int second, long number, int lenght)
{
    string result;
    if ((first == 3) && (second == 4 || second == 7) && (lenght == 15))
    {
        result = "AMEX\n";
    }
    else if ((first == 5) && (second == 1 || second == 2 || second == 3 || second == 4 || second == 5) && (lenght == 16))
    {
        result = "MASTERCARD\n";
    }
    else if ((first == 4) && (lenght == 13 || lenght == 16))
    {
        result = "VISA\n";
    }
    else
    {
        result = "INVALID\n";
    }
    return result;
}


//Get number of digit in number
int lenght(long number)
{
    int count = 0;
    while (number != 0)
    {
        number /= 10;
        count++;
    }
    return count;
}