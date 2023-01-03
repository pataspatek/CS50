#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

string encrypt(string text, string key);

int main(int argc, string argv[])
{
    //Takes the second Command Line Argument (=CLA) for the key.
    string key = argv[1];

    //Checks if there are only two CLA (first: ./substitution, second: key).
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    //Checks the lenght of the key. There are only 26 letter in the alphabet.
    else if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else
    {
        for (int j = 0; j < strlen(key); j++)
        {
            if (!isalpha(key[j]))
            {
                return 1;
            }
            else
            {
                for (int k = j + 1; k < strlen(key); k++)
                {
                    //Checks for duplicates in a code.
                    if (key[j] == key[k])
                    {
                        printf("Usage: ./substitution key\n");
                        return 1;
                    }
                }
            }
        }
    }
    string text = get_string("plaintext: ");
    string cipher = encrypt(text, key);
    printf("ciphertext: %s\n", cipher);
}

//Encrypts the given text according to the given key.
string encrypt(string text, string key)
{
    int index;
    for (int i = 0; i < strlen(text); i++)
    {
        //Takes lowercase letter.
        if (islower(text[i]))
        {
            //Finds the index of the letter using ASCII.
            index = text[i] - 'a';
            //Changes the letter according to the same index letter in the key.
            //Converts the letter back to the lowercase if necessary.
            text[i] = tolower(key[index]);
        }
        //Takes uppercase letter.
        else if (isupper(text[i]))
        {
            //Finds the index of the letter using ASCII.
            index = text[i] - 'A';
            //Changes the letter according to the same index letter in the key.
            //Converts the letter back to the uppercase if necessary.
            text[i] = toupper(key[index]);
        }

    }
    return text;
}