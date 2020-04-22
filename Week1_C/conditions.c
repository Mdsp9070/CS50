#include <stdio.h>
#include <cs50.h>

int main (void) {
    int x = get_int("n: ");
    int y = get_int("\ny: ");

    if (x > y) printf("\n\nx is greater than y\n");
    else if (x < y) printf("\n\nx is less than y\n");
    else printf("\n\nx is equals to y\n");
}
