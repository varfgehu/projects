from sys import argv, exit
import csv

if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

#read dna sequence
dna_file = open(argv[2], "r")
dna_reader = csv.reader(dna_file)
for row in dna_reader:
    dna_list = row

dna = dna_list[0] #store in srting

sequences = {} # create a dictionry where we will sotre the sequences we intended to count

database_file = open(argv[1], 'r')
people = csv.reader(database_file)
for row in people:
    dna_sequences = row
    dna_sequences.pop(0)
    break

for item in dna_sequences:
    sequences[item] = 1


#try to assemble to longest from each sequence by multipplying them and searched in the dna

for key in sequences:
    k = 1
    while(key*k in dna):
        k += 1
    sequences[key] = k - 1

for person in people:
    match = 0
    list_element = 1
    for ize in sequences:
        if sequences[ize] == int(person[list_element]):
            match += 1
            list_element += 1
    if match == len(sequences):
        print(person[0])
        exit()

print("No match")