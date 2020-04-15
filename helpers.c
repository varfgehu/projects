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

            new_gray = round(((float)origi_red + (float)origi_green + (float)origi_blue) / 3.0);

            image[row][column].rgbtRed = new_gray;
            image[row][column].rgbtGreen = new_gray;
            image[row][column].rgbtBlue = new_gray;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int origi_red, origi_green, origi_blue;
    int sepia_red, sepia_green, sepia_blue;

    for(int row = 0; row < height; row++ )
    {
        for(int column = 0; column < width; column++)
        {
            origi_red = image[row][column].rgbtRed;
            origi_green = image[row][column].rgbtGreen;
            origi_blue = image[row][column].rgbtBlue;

            sepia_red = round(((float)origi_red * 0.393) + ((float)origi_green * 0.769) + ((float)origi_blue * 0.189));
            sepia_green = round(((float)origi_red * 0.349) + ((float)origi_green * 0.686) + ((float)origi_blue * 0.168));
            sepia_blue = round(((float)origi_red * 0.272) + ((float)origi_green * 0.534) + ((float)origi_blue * 0.131));

            if(sepia_red > 255)
            {
                sepia_red = 255;
            }

            if(sepia_green > 255)
            {
                sepia_green = 255;
            }

            if(sepia_blue > 255)
            {
                sepia_blue = 255;
            }

            image[row][column].rgbtRed = sepia_red;
            image[row][column].rgbtGreen = sepia_green;
            image[row][column].rgbtBlue = sepia_blue;
        }
    }
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
