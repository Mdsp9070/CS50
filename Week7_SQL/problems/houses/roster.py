from sys import argv
from cs50 import SQL

db = SQL('sqlite:///students.db')

if len(argv) != 2:
    print('error, wrong arguments')
    print('usage: python roster.py <house name>!')
    exit()

house = argv[1]

data = db.execute('SELECT * FROM students ORDER BY last')

for index in data:
    if index['house'] == house:
        if index['middle'] != None:
            print(
                f"{index['first']} {index['middle']} {index['last']}, born {index['birth']}")
        else:
            print(
                f"{index['first']} {index['last']}, born {index['birth']}")
