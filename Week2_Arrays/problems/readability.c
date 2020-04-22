#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sent(string text);
float get_avgByWord(int n, int w);

int main(void) {
    string text = get_string("Text: ");
    int l = 0, w = 0, s = 0;
    float index = 0;

    l = count_letters(text);
    w = count_words(text);
    s = count_sent(text);

    float lByW = get_avgByWord(l, w);
    float sByW = get_avgByWord(s, w);

    index = ((0.0588 * lByW) - (0.296 * sByW)) - 15.8;

    /*printf("\n%d letter(s)", l);
    printf("\n%d word(s)", w);
    printf("\n%d sentence(s)", s);*/
    if (index >= 16) printf("\nGrade 16+\n");
    else if (index < 1) printf("\nBefore Grade 1\n");
    else printf("\nGrade %d\n", (int) round(index));
}

int count_letters(string text) {
    int letter = 0;
    for (int i = 0, n = strlen(text); i < n; i++) {
        if (isalpha(text[i])) letter++;
    }

    return letter;
}

int count_words(string text) {
    int word = 1;
    for (int i = 0, n = strlen(text); i < n; i++) {
        if (isblank(text[i])) word++;
    }

    return word;
}

int count_sent(string text) {
    int sentence = 0;
    for(int i = 0, n = strlen(text); i < n; i++) {
        switch(text[i]) {
            case '.':
            case '!':
            case '?':
                sentence++;
                break;
            default:
                break;
        }
    }

    return sentence;
}

float get_avgByWord(int n, int w) {
    float avg = ((float) n / w) * 100;

    return avg;
}