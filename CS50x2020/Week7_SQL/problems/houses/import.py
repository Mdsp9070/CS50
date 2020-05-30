from sys import argv
from cs50 import SQL
from csv import reader

if len(argv) != 2:
    print('error, wrong arguments')
    print('usage: python import.py *.csv!')
    exit()

db = SQL('sqlite:///students.db')

with open(argv[1]) as students:
    data = reader(students)
    next(data)
    for row in data:
        data = row[0].split()
        if len(data) < 3:
            db.execute("INSERT INTO students (first, last, house, birth) VALUES(?, ?, ?, ?)",
                       data[0], data[1], row[1], row[2])
        else:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       data[0], data[1], data[2], row[1], row[2])
