#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int origi_red, origi_green, origi_blue;
    int new_gray;

    for(int row = 0; row < height; row++ )
    {
        for(int column = 0; column < width; column++)
        {
            origi_red = image[row][column].rgbtRed;
            origi_green = image[row][column].rgbtGreen;
            origi_blue = image[row][column].rgbtBlue;

            //printf("rgbtRed: %i\n", image[row][column].rgbtRed);
            //printf("rgbtGreen: %i\n", image[row][column].rgbtGreen);
            //printf("rgbtBlue: %i\n", image[row][column].rgbtBlue);

            new_gray = round(((float)origi_red + (float)origi_green + (float)origi_blue) / 3.0);
            //printf("new_gray: %i\n", new_gray);

            image[row][column].rgbtRed = new_gray;
            image[row][column].rgbtGreen = new_gray;
            image[row][column].rgbtBlue = new_gray;

            //printf("After filtering\n");
            //printf("rgbtRed: %i\n", image[row][column].rgbtRed);
            //printf("rgbtGreen: %i\n", image[row][column].rgbtGreen);
            //printf("rgbtBlue: %i\n", image[row][column].rgbtBlue);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
