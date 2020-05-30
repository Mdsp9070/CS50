#include <stdio.h>
#include <cs50.h>

int main (void) {
    int age = get_int("What'st your age?\n");
    printf("You're at least %d days old!\n", age * 365);
}
