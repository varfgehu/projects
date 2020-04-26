import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "POST":
        return apology("what is POST at index?!", 403)

    # get username from database by session id
    result = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
    username = result[0]["username"]

    # Query the stocks' and the number of shares the user owns from the database
    stocks = db.execute("SELECT symbol, SUM(shares) FROM buy WHERE username= :username GROUP BY symbol", username = username)

    grand_total = 0

    for stock in stocks:
        # Get stock name by symbol
        result = lookup(stock["symbol"])
        total = int(stock["SUM(shares)"] * float(result["price"]))
        grand_total += total

        print(stock)

        stock["symbol"] = result["symbol"]
        stock["name"] = result["name"]
        stock["price"] = result["price"]
        stock["total"] = str(usd(total))

    # Add CASH to stocks
    cash_total = db.execute("SELECT cash FROM users WHERE username = :username", username=username)
    stocks.append({"symbol" : "CASH", "total": usd(float(cash_total[0]["cash"]))})

    print(float(cash_total[0]["cash"]))

    grand_total += float(cash_total[0]["cash"])

    print(stocks)
    print(grand_total)

    return render_template("index.html", stocks=stocks, grand_total=usd(grand_total))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check if the number of shares is filled
        if ((int(request.form.get("shares"))) <= 0):
            print("Number of shares selecte: " + (request.form.get("shares")))
            return apology("must provide number of shares")

        # Get the selected stock's price
        result = lookup(request.form.get("symbol"))
        if not result:
            return apology("not a valid symbol", 403)

        symbol=result["symbol"]

        price = result["price"]
        print(price)

        # Get username by session id

        # get username from database by session id
        result = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        username = result[0]["username"]

        # Get the amount of cash the user's have
        result = db.execute("SELECT cash FROM users WHERE username= :username", username = username )
        user_cash = float(result[0]["cash"])

        # if user can buy that amount -> INSERT to finance.db database the following informations: username, symbol, price (for 1 stock), shares (number of ), datetime
        # update the cash for the user

        if (user_cash >= float(price) * int(request.form.get("shares"))):
            now = datetime.now()
            price_float=float(price)
            shares=int(request.form.get("shares"))
            datetime_now=(now.strftime("%Y-%m-%d %H:%M:%S"))

            db.execute("INSERT INTO buy (username, symbol, price, shares, datetime) VALUES (:username, :symbol, :price, :shares, :datetime)", username=username, symbol=symbol, price=price_float, shares=shares, datetime=datetime_now)
            db.execute("UPDATE users SET cash = :cash WHERE username = :username", username=username, cash=user_cash-((price_float*(shares))))
            # kell egy adatbázistábla, ahol a userek összesített stock anyaga számlálódik, vagy a historyból kell kihámozni
        else:
            return apology("not enaught cash", 403)

        return redirect("/")

    # User reached route via EGT (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # get username from database by session id
    result = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
    username = result[0]["username"]

    rows = db.execute("SELECT * FROM buy WHERE username= :username ORDER BY datetime DESC", username=username)

    return render_template("history.html", rows=rows)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("you must provide a symbol", 403)

        result = lookup(request.form.get("symbol"))

        if not result:
            return apology("not a valid symbol", 403)

        return render_template("quote.html", name=result["name"], symbol=result["symbol"], price=usd(int(result["price"])))


    else:

        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Create local variables for username and password
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 403)

        # Ensure confirmation for password was submitted
        if not request.form.get("confirmation"):
            return apology("must provide confirmation of your password", 403)

        # Ensure password and confirmation are the same
        if request.form.get("confirmation") != password:
            return apology("password and confirmation are not the same", 403)

        # Query database for username:
        rows = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))

        # Ensure username is not in the database
        if len(rows) != 0:
            return apology("Sorry, the username is already used", 403)

        # INSERT into database
        db.execute("INSERT INTO users (username, hash) VALUES (:name, :password)", name=username, password=generate_password_hash(password))

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # get username from database by session id
        result = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        username = result[0]["username"]

        # Is the symbol valid?
        result = lookup(request.form.get("symbol"))
        symbol = result["symbol"]
        price = result["price"]

        # Do the user owns the stock in the needed amount (amount is positive integer)?
        result = db.execute("SELECT symbol, SUM(shares) FROM buy WHERE username= :username AND symbol= :symbol", username=username, symbol=symbol)
        print(result)
        if not result[0]["SUM(shares)"]:
            return apology("user does not onw that stock", 403)

        desired_shares = request.form.get("shares")
        if int(desired_shares) < 0:
            return apology("must provide positive number of shares", 403)

        if int(desired_shares) > int(result[0]["SUM(shares)"]):
            return apology("owner does not own that amount", 403)

        desired_shares = int(desired_shares) * (-1)
        print(desired_shares)

        now = datetime.now()
        price_float=float(price)
        datetime_now=(now.strftime("%Y-%m-%d %H:%M:%S"))

        # INSERT the transaction into buy database
        db.execute("INSERT INTO buy (username, symbol, price, shares, datetime) VALUES (:username, :symbol, :price, :shares, :datetime)", username=username, symbol=symbol, price=price, shares=desired_shares, datetime=datetime_now)

        # UPDATE the cash for the user
        # Get the amount of cash the user's have
        result = db.execute("SELECT cash FROM users WHERE username= :username", username = username )
        user_cash = float(result[0]["cash"])

        new_cash = user_cash + (price_float * float(desired_shares * (-1)))
        db.execute("UPDATE users SET cash = :cash WHERE username = :username", username=username, cash=new_cash)

        return redirect("/")

    else:
        return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
