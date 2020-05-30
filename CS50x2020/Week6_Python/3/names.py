# Implements linear search for names

from sys import exit

# A list of names
names = ["EMMA", "RODRIGO", "BRIAN", "DAVID"]

# Search for EMMA
if "EMMA" in names:
    print("Found")
    exit(0)
print("Not found")
exit(1)
