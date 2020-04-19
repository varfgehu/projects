from cs50 import get_int

heigth = get_int("Heigth: ")

while(heigth < 1 or heigth > 8):
    heigth = get_int("Heigth: ")

for i in range(heigth):
    print(" " * (heigth-i+1), end="")
    print("#" * (i+1), end="")
    print()
