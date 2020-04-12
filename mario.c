#include <cs50.h>
#include <stdio.h>

void print_hashmark(int repeat);
void print_new_line(void);
void print_space(int repeat);

int main(void)
{
    int height;

    do
    {
        height = get_int("Height: ");

        if (height >= 1 && height <= 8)
        {
            for (int i = 1; i <= height; i++)
            {
                print_space(height - i);
                print_hashmark(i);
                print_new_line();
            }
        }
    }
    while (height < 1 || height > 8);   
}

void print_hashmark(int repeat)
{
    for(int i = 0; i <repeat; i++)
    {
        printf("#");
    }
}

void print_new_line(void)
{
    printf("\n");
}

void print_space(int repeat)
{
    for (int i = 0; i < repeat; i++)
    {
        printf(" ");
    }
}

