// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 1000;

// Hash table
node *table[N];

// Word count in a dictionary
int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int code = hash(word);

    node *cursor = table[code];

    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }

        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int value = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        value += tolower(word[i]);
    }

    return value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open a dictionary
    FILE *file = fopen(dictionary, "r");

    // Check for NULL return
    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];

    // Scan the words from the dictionary until EOF
    while (fscanf(file, "%s", word) != EOF)
    {
        // Create a temporary node and allocate a memory for it
        node *tempnode = malloc(sizeof(node));
        if (tempnode == NULL)
        {
            return false;
        }

        // Copy the word from the dictionary into the temporary node
        strcpy(tempnode->word, word);

        int code = hash(word);

        if (table[code] == NULL)
        {
            tempnode->next = NULL;
            table[code] = tempnode;
        }
        else
        {
            tempnode->next = table[code];
            table[code] = tempnode;
        }
        word_count++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
        table[i] = NULL;
    }
    return true;
}
