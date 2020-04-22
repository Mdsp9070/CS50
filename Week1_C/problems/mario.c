#include <stdio.h>
#include <cs50.h>

void pyramid(int); //initialize pyramid funtion

int main(void) {
    int h;
    do {
        h = get_int("Height: "); //get h from user input
    } while(h < 1 || h > 8); //only accepts numbers 1 trough 8

    pyramid(h); //pass h as pyramid argument
}

void pyramid(int h) {
    for (int i = 1; i <= h; i++) { //first loop, for columns
       for ( int space = 0; space < h - i; space++ ) { //second loop, for spaces between each '#'
           printf (" ");
       }
       for (int j = 0; j < i; j ++) { //when space loop is done, starts the third loop, for print first pyramid rows
           printf("#");
       }
       printf("  "); //separete each pyramid
       for (int j = 0; j < i; j ++) { //prints second pyramid
           printf("#");
       }
       printf("\n");
    }
}

