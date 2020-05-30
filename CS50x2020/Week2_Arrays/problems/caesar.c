#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int validateKey(int argc, string argv[]);
string encrypt(int key, string plain);

int main(int argc, string argv[]) {
    string pText, eText;
    int key = validateKey(argc, argv);
    if (!key) return 1;
    else {
        pText = get_string("plain text: ");
        eText = encrypt(key, pText);
        printf("ciphertext: %s\n", eText);
    }
}

int validateKey(int argc, string argv[]) {
    int key = 0;

    if (argc == 2) {
        for (int i = 0, n = strlen(argv[1]); i < n; i++) {
            if (!isdigit(argv[1][i])) {
                printf("Usage: ./caesar key");
                return 0;
            }
        }
        key = atoi(argv[1]);
        return key;
    }
    else {
        printf("Usage: ./caesar key");
        return 0;
    }
}

string encrypt(int key, string plain) {
    char ch;
    for(int i = 0; plain[i] != '\0'; ++i){
		ch = plain[i];

		if(ch >= 'a' && ch <= 'z'){

			if(ch += key > 'z') {
			    ch -= 97;
				ch = ((ch + key) % 26) + 97;
			}
			if(ch > 'z'){

				ch -= 97;
				ch = ((ch + key) % 26) + 97 - 1;
			}

			plain[i] = ch;
		}
		else if(ch >= 'A' && ch <= 'Z'){
            if(ch += key > 'Z') {
			    ch -= 65;
				ch = ((ch + key) % 26) + 65;
			}
			if(ch > 'Z'){

				ch -= 65;
				ch = ((ch + key) % 26) + 65 - 1;
			}

			plain[i] = ch;
		}
	}
	return plain;
}