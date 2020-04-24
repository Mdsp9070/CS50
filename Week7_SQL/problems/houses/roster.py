from sys import argv
from cs50 import SQL

db = SQL('sqlite:///students.db')

if len(argv) != 2:
    print('error, wrong arguments')
    print('usage: python roster.py <house name>!')
    exit()

house = argv[1]

