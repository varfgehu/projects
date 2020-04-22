from cs50 import SQL
import csv
from sys import argv, exit

if len(argv) != 2:
    print("Usage: python import.py [House]")
    exit(1)

db = SQL("sqlite:///students.db")

house = argv[1]

students = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house)

for student in students:
    if student['middle'] == "None":
        print(student['first'] + " " + student['last'] + ", born in " + str(student['birth']))
    else:
        print(student['first'] + " " + student['middle'] + " " + student['last'] + ", born in " + str(student['birth']))
