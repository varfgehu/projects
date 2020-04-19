from cs50 import get_int

heigth = get_int("Heigth: ")

while(heigth < 1 or heigth > 8):
    heigth = get_int("Heigth: ")

for i in range(1, heigth+1):
    print(" " * (heigth-i), end="")
    print("#" * (i), end="")
    print()
