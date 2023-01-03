#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    //Ask user for an input text.
    string text = get_string("Text: ");

    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    //Coleman-Liau index
    float index = (0.0588 * letters / words * 100) - (0.296 * sentences / words * 100) - 15.8;

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index <= 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
}

//Counts the number of letter in a given text.
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        //Letters counter will increase only if the the element is uppercase or lowercase letter.
        if (islower(text[i]) || isupper(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

//Counts the number of words in a given text.
int count_words(string text)
{
    int words = 1;
    for (int j = 0; j < strlen(text); j++)
    {
        //Assume that the sentence does not start or end with a space and there are not double spaces.
        if (text[j] == 32)
        {
            words++;
        }
    }
    return words;
}

//Counts the number of sentences in a given text.
int count_sentences(string text)
{
    int sentences = 0;
    for (int k = 0; k < strlen(text); k++)
    {
        //Assume that the sentence is a sequence of characters ending with period, exclamation point or question mark.
        //Does not take in count perion inside of the sentence like Mr.
        if (text[k] == 33 || text[k] == 46 || text[k] == 63)
        {
            sentences++;
        }
    }
    return sentences;
}