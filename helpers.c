#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define UPPER_LIMIT 255

void check_for_upper_limit(int *color);
void set_pixel_blury(int row, int column, int heigth, int width, RGBTRIPLE image[heigth][width], RGBTRIPLE copied_image[heigth][width]);

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
void blur(int heigth, int width, RGBTRIPLE image[heigth][width])
{
    int i = 0;
    RGBTRIPLE copied_image[heigth][width];

    memcpy(&copied_image, image, sizeof(copied_image));

    //printf("[0][0] image: [%i][%i][%i] copy: [%i][%i][%i]", image[0][0].rgbtRed,image[0][0].rgbtGreen, image[0][0].rgbtBlue, copied_image[0][0].rgbtRed, copied_image[0][0].rgbtGreen, copied_image[0][0].rgbtBlue);

    for(int row = 0; row </*1*/heigth; row++ )
    {
        for(int column = 0; column < /*1*/width; column++)
        {
            set_pixel_blury(row, column, heigth, width, image, copied_image);
        }
    }

    return;
}

void set_pixel_blury(int row, int column, int heigth, int width, RGBTRIPLE image[heigth][width], RGBTRIPLE copied_image[heigth][width] )
{
    int sum_red = 0, sum_green = 0, sum_blue = 0;
    int index = 0;
    //printf("pixel[%i][%i]\n", row, column);
    //printf("Neighbors:\n");

    for(int i = -1; i <= 1; i++)
    {
        for (int j = - 1; j <= 1; j++)
        {
            //printf("[%i][%i] -->", row + i, column + j);

            if((row + i >= 0 && column + j >= 0) && (row + i < heigth && column + j < width))
            {
                //printf("Valid pixel --> R:%i, G:%i, B:%i\n", copied_image[row + i][column + j].rgbtRed, copied_image[row + i][column + j].rgbtGreen, copied_image[row + i][column + j].rgbtBlue);

                sum_red += copied_image[row + i][column + j].rgbtRed;
                sum_green += copied_image[row + i][column + j].rgbtGreen;
                sum_blue += copied_image[row + i][column + j].rgbtBlue;

                index++;
            }
            else
            {
               //printf("Invalid pixel --> [%i][%i]\n", row, column);
            }
        }
    }

    //printf("index: %i\n", index);
    /*if(index == 0)
    {
        printf("index = 0, row: %i, column: %i", row, column);
    }*/

    image[row][column].rgbtRed = round((float)sum_red / (float)index);
    image[row][column].rgbtGreen = round((float)sum_green / (float)index);
    image[row][column].rgbtBlue = round((float)sum_blue / (float)index);

    //printf("average red: %i\n", image[row][column].rgbtRed);
    //printf("average green: %i\n", image[row][column].rgbtGreen);
    //printf("average blue: %i\n\n\n", image[row][column].rgbtBlue);

}
