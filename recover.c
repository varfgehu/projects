#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int is_jpeg_header_detected(BYTE buffer[512]);

int main(int argc, char *argv[])
{
    //check for invalide usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //open file
    FILE *file = fopen(argv[1], "r");
    if(file == NULL)
    {
        printf("%s file cannot be opened for reading\n", argv[1]);
        return 1;
    }

    BYTE buffer[512];
    int bytes_read;
    int file_opened = 0;
    char filename[7];
    FILE *img = NULL;
    int first_jpeg_found = 0;
    int jpeg_cnt = 0;

    do
    {
        bytes_read = fread(buffer, 1, 512, file);
        //printf("Inteded: %i, Actually read: %i\n", 512, bytes_read);
        if(1 == is_jpeg_header_detected(buffer))
        {
            printf("JPEG file header found\n");

            //first JPEG found
            if(0 == first_jpeg_found)
            {
                first_jpeg_found = 1;
                //1.compose filename
                //2.open file
                //3.start writing file

                sprintf(filename, "%03i.jpg", jpeg_cnt);

                img = fopen(filename, "w");

                fwrite(buffer, 1, bytes_read, img);
            }
            else
            {
                //this is not the firt jpeg found
                //1.close the actualy open file
                //2.compose next filename
                //3.open next file
                //4.start writing new file
                fclose(img);

                jpeg_cnt++;
                sprintf(filename, "%03i.jpg", jpeg_cnt);

                img = fopen(filename, "w");

                fwrite(buffer, 1, bytes_read, img);

            }
        }
        else
        {
            // no header detected
            if(img != NULL)
            {
                fwrite(buffer, 1, bytes_read, img);
            }
        }
    }
    while(bytes_read == 512);

}

int is_jpeg_header_detected(BYTE buffer[512])
{
    if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
    {
        return 1;
    }
    else
    {
        return 0;
    }

}
