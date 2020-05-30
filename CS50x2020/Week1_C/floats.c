#include <stdio.h>
#include <cs50.h>

int main(void) {
    float x = get_float("x: ");
    float y = get_float("\ny: ");

    printf("x / y = %.50f\n", x / y);
}
