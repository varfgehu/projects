#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define UPPER_LIMIT 255

void check_for_upper_limit(int *color);

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

            check_for_upper_limit(&sepia_red);
            check_for_upper_limit(&sepia_green);
            check_for_upper_limit(&sepia_blue);

            image[row][column].rgbtRed = sepia_red;
            image[row][column].rgbtGreen = sepia_green;
            image[row][column].rgbtBlue = sepia_blue;
        }
    }
    return;
}

void check_for_upper_limit(int *color)
{
    if(*color > UPPER_LIMIT)
    {
        *color = UPPER_LIMIT;
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int step = 0;
    int tmp_red, tmp_green, tmp_blue;
    int last;
    int left, right;

    for(int row = 0; row < height; row++)
    {
        step = 0;
        last = width - 1;

        do
        {
        left = step;
        right = last - step;

        int *tmp = malloc(3 * sizeof(int));
        tmp[0] = image[row][left].rgbtRed;
        tmp[1] = image[row][left].rgbtGreen;
        tmp[2] = image[row][left].rgbtBlue;

        image[row][left].rgbtRed = image[row][right].rgbtRed;
        image[row][left].rgbtGreen = image[row][right].rgbtGreen;
        image[row][left].rgbtBlue = image[row][right].rgbtBlue;

        image[row][right].rgbtRed = tmp[0];
        image[row][right].rgbtGreen = tmp[1];
        image[row][right].rgbtBlue = tmp[2];

        free(tmp);

        step++;
        }
        while(right - left >= 3);

    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
