#include <stdio.h>
#include <math.h>
#include <cs50.h>

int main(void) 
{
    float d;
    int coins = 0;

    do 
    {
        d = get_float("Change owed: ");
    } 
    while (d < 0);
    //get chage owed

    //gambiarra0
    if (d < 0.01)
    {
        d += 0.001;
    }
    //primeiro if
    if (d >= 0.25) 
    {
        coins += d / 0.25;
        d = fmod(d, 0.25);
        printf("\nd0: %.25f\n", d);
        printf("coins0: %d\n\n", coins);
    }
    //segundo if
    if (d >= 0.1) 
    {
        coins += d / 0.1;
        d = fmod(d, 0.1);
        printf("\nd1: %.25f\n", d);
        printf("coins1: %d\n\n", coins);
    }
    //terceiro if
    if (d >= 0.05) 
    {
        coins += d / 0.05;
        //gambiarra1
        d = fmod(d, 0.05) + 0.001;
        printf("\nd2: %.25f\n", d);
        printf("coins2: %d\n\n", coins);
    }
    //quarto if
    if (d >= 0.01) 
    {
        coins += d / 0.01;
        d = fmod(d, 0.01);
        printf("\nd3: %.25f\n", d);
        printf("coins3: %d\n\n", coins);
    }

    printf("coins: %d\n", coins);
}
