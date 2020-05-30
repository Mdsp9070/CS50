#include <stdio.h>
#include <cs50.h>

int main (void) {
    printf("Hello, World!!!\n");
    string answer = get_string("What's your name?\n");
    printf("Hi %s, how are you?\n", answer);
}
