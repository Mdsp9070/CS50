#include <stdio.h>
#include <cs50.h>

void cough (int);

int main(void) {
    int n = get_int("How many times you want to cough?\n");
    cough(n);
}

void cough (int n) {
    for (int i = 0; i < n; i++) {
        printf("cough\n");
    }
}
