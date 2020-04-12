// greet user

#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // ask the user's name
    string name = get_string("What is your name?\n");
    
    //print the user's name to terminal
    printf("hello, %s\n", name);
}
