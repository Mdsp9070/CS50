from sys import argv
from csv import reader, DictReader

if len(argv) != 3:
    print('error, incorrect parameters')
    print('usage: dna.py database.csv sequence.txt')
    exit()

with open(argv[2]) as txt:
    dna = txt.read()

with open(argv[1]) as database:
    content = reader(database)
    for row in content:
        l = row
        l.pop(0)
        break

sequence = {}

for i in l:
    sequence[i] = 1

for key in sequence:
    l = len(key)
    tempMax = 0
    temp = 0
    for i in range(len(dna)):
        # after having counted a sequence it skips at the end of it to avoid counting again
        while temp > 0:
            temp -= 1
            continue

        # if the segment of dna corresponds to the key and there is a repetition of it we start counting
        if dna[i: i + l] == key:
            while dna[i - l: i] == dna[i: i + l]:
                temp += 1
                i += l

            # it compares the value to the previous longest sequence and if it is longer it overrides it
            if temp > tempMax:
                tempMax = temp

    # store the longest sequence in the dictionary using the correspondent key
    sequence[key] += tempMax
# open and iterate trough the database of people treating each one like a dictionary so it can compare to the sequence one
with open(argv[1], newline='') as peoplefile:
    people = DictReader(peoplefile)
    for person in people:
        match = 0
        # compares the sequence to every person and prints name before leaving the program if there is a match
        for dna in sequence:
            if sequence[dna] == int(person[dna]):
                match += 1
        if match == len(sequence):
            print(person['name'])
            exit()

    print("No match")
