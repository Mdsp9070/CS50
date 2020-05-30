#include <stdio.h>
#include <unistd.h>
#include <cs50.h>

int main(void) {
    for (int i = 1; ; i *= 2) {
        printf("%i\n", i);
        sleep(1);
    }
}
