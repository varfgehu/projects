from cs50 import SQL
import csv
from sys import argv, exit

if len(argv) != 2:
    print("Usage: python import.py csv file")
    exit(1)

db = SQL("sqlite:///students.db")

#open CSV file for reading
with open(argv[1], "r") as characters:
    #Use csv module
    reader = csv.DictReader(characters)

    for row in reader:
        name = row['name'].split(" ")
        if len(name) == 2:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
            name[0], (None,), name[1], row['house'], row['birth'])
        else:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
            name[0], name[1], name[2], row['house'], row['birth'])
