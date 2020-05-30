import re
from cs50 import get_string
from sys import exit

t = get_string('Text: ')
l = len(re.findall('[a-zA-Z]', t))
w = len(re.findall('\s', t)) + 1
s = len(re.findall('[.!?]', t))

avgL = (l / w) * 100
avgS = (s / w) * 100

g = round((.0588 * avgL) - (.296 * avgS) - 15.8)

if g >= 16:
    print('Grade 16+')
    exit()
if g < 1:
    print('Before Grade 1')
    exit()
print(f'Grade {g}')
