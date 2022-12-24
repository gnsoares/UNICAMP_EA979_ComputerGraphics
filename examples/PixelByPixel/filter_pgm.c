/* draw a color image */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

void put_byte(int output) {
    int status = putchar(output);
    if (status == EOF) {
        fprintf(stderr, "error writing to output stream\n");
        exit(EXIT_FAILURE);
    }
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        fprintf(stderr,
            "usage: filter_pgm < input.pgm > output.pgm\n"
            "filters a PGM image pixel by pixel\n");
        return EXIT_FAILURE;
    }

    // Defines image header
    int width;
    int height;
    int max_val;

    // Reads output header
    if (!(getchar() == 'P' && getchar() == '5' && getchar() == '\n')) {
        fprintf(stderr, "invalid magic number on input image header");
        return EXIT_FAILURE;
    }
    scanf("%d %d\n", &width, &height);
    scanf("%d\n", &max_val);
    if (max_val > 255) {
        fprintf(stderr, "cannot handle images with max_val > 255");
        return EXIT_FAILURE;
    }

    // Writes output header
    printf("P5\n");
    printf("%d %d\n", width, height);
    printf("%d\n", max_val);

    // Outputs image
    for (int row=0; row<height; row++) {
        for (int col=0; col<width; col++) {
            int input_pixel = getchar();
            int output_pixel;
            output_pixel = input_pixel; // Make transformation here
            output_pixel = (output_pixel <= max_val) ? output_pixel : max_val;
            output_pixel = (output_pixel >= 0)       ? output_pixel : 0;
            put_byte(output_pixel);
        }
    }

    return EXIT_SUCCESS;
}

