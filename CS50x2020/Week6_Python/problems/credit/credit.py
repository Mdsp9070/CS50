from cs50 import get_string
from sys import exit

n = get_string('Number: ')
x = [int(d) for d in n]
s1 = 0
s2 = 0

for i in range(0, len(x), 2):
    if x[i] * 2 > 9:
        tmp = x[i] * 2
        y = [int(d) for d in str(tmp)]
        s1 += y[0] + y[1]
    else:
        s1 += x[i] * 2

for j in range(1, len(x), 2):
    s2 += x[j]

st = s1 + s2

if x[0] == 3 and (x[1] == 4 or x[1] == 7):
    print('AMEX')
elif x[0] == 4:
    print('VISA')
elif x[0] == 5:
    for x[1] in [1, 2, 3, 4, 5]:
        print('MASTERCARD')
        break
else:
    if st % 10 != 0:
        print('INVALID')
