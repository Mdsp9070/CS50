from cs50 import get_float
from math import ceil

while True:
    d = get_float("Change owed: ")
    if d > 0:
        break
d *= 100

quarters = d // 25
d %= 25
dimes = d // 10
d %= 10
nickels = d // 5
d %= 5
pennies = d // 1

print(f'coins: {round(quarters+dimes+nickels+pennies)}')
