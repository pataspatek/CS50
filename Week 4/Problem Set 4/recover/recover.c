#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

//Number of bytes in one block in the memory card
const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // Checks for exactly one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover card.raw\n");
        return 1;
    }

    // Open file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 2;
    }

    // Set the output pointer to NULL
    FILE *output = NULL;

    // Create an array with 512 elements (bytes)
    BYTE buffer[BLOCK_SIZE];

    // Count jpg files found
    int i = 0;

    // Store jpg files named: ###.jpg'\0'
    char filename[8];

    // Read from the memory card into the buffer until no 512 byte block are found
    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        // Check if jpg is found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If output already open, close it
            if (output != NULL)
            {
                fclose(output);
            }
            // Create jpg files
            sprintf(filename, "%03i.jpg", i);
            output = fopen(filename, "w");
            i++;

        }
        if (output != NULL)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, output);
        }
    }

    if (output != NULL)
    {
        fclose(output);
    }

    fclose(file);

    return 0;
}