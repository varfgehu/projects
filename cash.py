from cs50 import get_float


coins = 0

quarter = 25
dime = 10
nickel = 5
penny = 1

cash_in_dollar = get_float("Change owed: ")

while(cash_in_dollar < 0):
    cash_in_dollar = get_float("Change owed: ")


cash_in_cents = int(cash_in_dollar*100)

while(cash_in_cents > 0):
    if(int(cash_in_cents / quarter) > 0):
        print("quarters needed")
        quarters = int(cash_in_cents / quarter)
        cash_in_cents = cash_in_cents - (quarter * quarters)
        coins += quarters
        print("quarters needed: " + str(quarters) + " cash remains: " + str(cash_in_cents))

    if(int(cash_in_cents / dime) > 0):
        print("dimes needed")
        dimes = int(cash_in_cents / dime)
        cash_in_cents = cash_in_cents - (dime * dimes)
        coins += dimes
        print("dimes needed: " + str(dimes) + " cash remains: " + str(cash_in_cents))

    if(int(cash_in_cents / nickel) > 0):
        print("nickels neeeded")
        nickels = int(cash_in_cents / nickel)
        cash_in_cents = cash_in_cents - (nickel * nickels)
        coins += nickels
        print("nickels needed: " + str(nickels) + " cash remains: " + str(cash_in_cents))

    if(int(cash_in_cents / penny) > 0):
        print("pennies neeeded")
        pennies = int(cash_in_cents / penny)
        cash_in_cents = cash_in_cents - (penny * pennies)
        coins += pennies
        print("pennies needed: " + str(pennies) + " cash remains: " + str(cash_in_cents))

print(coins)