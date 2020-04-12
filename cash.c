#include <stdio.h>
#include <math.h>
#include <cs50.h>

int main(void)
{
    int coins = 0;
    float dollar = 0.0;
    do
    {
        dollar = get_float("Change owed: ");

        if (dollar > 0.00)
        {
            int cents = round(dollar * 100);

            int quarters = cents / 25;
            if (quarters > 0)
            {
                coins += quarters;
                cents = cents - (quarters * 25);
            }

            int dimes = cents / 10;
            if (dimes > 0)
            {
                coins += dimes;
                cents = cents - (dimes * 10);
            }

            int nickels = cents / 5;
            if (nickels > 0)
            {
                coins += nickels;
                cents = cents - (nickels * 5);
            }

            int pennies = cents / 1;
            if (pennies > 0)
            {
                coins += pennies;
            }

            printf("%i\n", coins);
        }
    }
    while (dollar < 0.00);
}
