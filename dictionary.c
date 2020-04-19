// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26 * 26 * 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int hash_index = hash(word);

    for (node *tmp = table[hash_index]; tmp != NULL; tmp = tmp->next)
    {
        if (0 == strcasecmp(tmp->word, word))
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int length = 0;
    char lowercase_word[2] = {0};
    int hunderds = 0;
    int tens = 0;
    int ones = 0;

    length = strlen(word);

    if (1 == length)
    {
        if (word[0] >= 'A' && word[0] <= 'Z')
        {
            lowercase_word[0] = word[0] + 32;
        }
        else if (word[0] >= 'a' && word[0] <= 'z')
        {
            lowercase_word[0] = word[0];
        }
        else
        {
            lowercase_word[0] = '\0';
        }


        ones = (lowercase_word[0] - 97) * 1;

        return (ones);
    }
    else// if(2 == length)
    {

        if (word[0] >= 'A' && word[0] <= 'Z')
        {
            lowercase_word[0] = word[0] + 32;
        }
        else if (word[0] >= 'a' && word[0] <= 'z')
        {
            lowercase_word[0] = word[0];
        }
        else
        {
            lowercase_word[0] = '\0';
        }

        if (word[1] >= 'A' && word[1] <= 'Z')
        {
            lowercase_word[1] = word[1] + 32;
        }
        else if (word[1] >= 'a' && word[1] <= 'z')
        {
            lowercase_word[1] = word[1];
        }
        else
        {
            lowercase_word[1] = lowercase_word[0];
        }

        tens = (lowercase_word[1] - 97) * 26;
        ones = (lowercase_word[0] - 97) * 1;

        return (tens + ones);
    }

}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    int i = 0;
    int hash_index = 0;
    char word[LENGTH + 1];

    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    while (EOF != fscanf(file, "%s", word))
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }

        new_node->next = NULL;
        strcpy(new_node->word, word);

        hash_index = hash(word);

        if (table[hash_index] == NULL)
        {
            //first node in the [hash_index] array, simply create a node
//            printf("First node for table[%i], creating..\n\n", hash_index);
            table[hash_index] = new_node;
        }
        else
        {
            // not the first node in the [hash_index] array, insert
//            printf("Not the first node for table[%i], inserting..\n\n", hash_index);
            new_node->next = table[hash_index];
            table[hash_index] = new_node;
        }
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    int i = 0;
    unsigned int sum = 0;

    while (i < 26 * 26 * 26)
    {
        if (table[i] != NULL)
        {
            for (node *tmp = table[i]; tmp != NULL; tmp = tmp->next)
            {
                sum++;
            }
        }
        i++;
    }

    return sum;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *cursor = NULL;
    node *tmp = NULL;

    cursor = table[0];
    tmp = table[0];

    for (int i = 0; i < 26 * 26 * 26; i++)
    {
        if (table[i] != NULL)
        {
            cursor = table[i];
            tmp = table[i];

            do
            {
                cursor = cursor->next;
                free(tmp);

                tmp = cursor;

            }
            while (tmp != NULL);
        }
    }

    return true;
}
