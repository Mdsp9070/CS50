from cs50 import get_int

while True:
    n = get_int("Height: ")
    if n > 0 and n < 9:
        break
k = n - 1

for i in range(n):
    for j in range(k):
        print(end=' ')
    k -= 1
    for j in range(i+1):
        print('#', end='')
    print('  ', end='')
    for j in range(i+1):
        print('#', end='')
    print()
