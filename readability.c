#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

float calculate_l(float letters, float words);
float calculate_s(float sentences, float words);
int calculate_index(float average_letter, float average_sentence);
void print_grade(int index);

int main(void)
{
    // get text input and print it out
    string text = get_string("Text: ");

    //count the letters
    int num_of_letters = count_letters(text);

    // count words
    int num_of_words = count_words(text);

    //count sentences
    int num_of_sentences = count_sentences(text);

    //calculate averages
    float average_letter = calculate_l(num_of_letters, num_of_words);
    float average_sentence = calculate_s(num_of_sentences, num_of_words);

    //calculate index
    int index = calculate_index(average_letter, average_sentence);


    print_grade(index);
}


int count_letters(string text)
{
    int num_of_letters = 0;
    for (int i = 0, length = strlen(text); i < length + 1; i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            num_of_letters++;
        }

    }

    return num_of_letters;
}

int count_words(string text)
{
    int num_of_words = 0;
    bool word_found = false;
    for (int i = 0, length = strlen(text); i < length + 1; i++)
    {
        //find the begining of a word
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            if (word_found == false)
            {
                num_of_words++;
            }

            word_found = true;
        }
        else if (text[i] == ' ')
        {
            word_found = false;
        }
        else
        {}
    }

    return num_of_words;
}

int count_sentences(string text)
{
    int num_of_sentences = 0;
    for (int i = 0, length = strlen(text); i < length + 1; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            num_of_sentences++;
        }

    }

    return num_of_sentences;
}

float calculate_l(float letters, float words)
{
    return (((float)letters / (float)words) * 100.0);
}

float calculate_s(float sentences, float words)
{
    return ((float)sentences / (float)words) * 100.0;
}

int calculate_index(float average_letter, float average_sentence)
{
    return round((0.0588 * average_letter) - (0.296 * average_sentence) - 15.8);
}

void print_grade(int index)
{
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}