#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

void terminate_program(void);

int main(int argc, string argv[] )
{
    if (argc != 2)
    {
        //printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        for(int i = 0, length = strlen(argv[1]); i < length; i++)
        {
            //printf("%c\n", argv[1][i]);
            if(argv[1][i] < '0' || argv[1][i] > '9')
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }

        int key = atoi(argv[1]) % 26;
        //printf("Key: %i", key);

        string plaintext = get_string("plaintext: ");

        printf("ciphertext: ");

        for(int i = 0, length = strlen(plaintext); i < length ; i++)
        {
            if (plaintext[i] >= 'a' && plaintext[i] <= 'z')
            {
                if( plaintext[i] + key > (int)'z' )
                {
                    printf("%c", key - ( (int)'z' - plaintext[i] ) - 1 + (int)'a');
                }
                else
                {
                    printf("%c", ( (int)plaintext[i] + key) );
                }
            }
            else if (plaintext[i] >= 'A' && plaintext[i] <= 'Z')
            {
                if( plaintext[i] + key > (int)'Z' )
                {
                    printf("%c", key - ( (int)'Z' - plaintext[i] ) - 1 + (int)'A');
                }
                else
                {
                    printf("%c", ( (int)plaintext[i] + key) );
                }
            }
            else
            {
                printf("%c", (int)plaintext[i]);
            }
        }

        printf("\n");



    }
}



