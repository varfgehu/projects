import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

from datetime import datetime
from random import randint
import time

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///travel.db")

@app.route("/")
@login_required
def index():
    if request.method == "GET":

        # Assemble poll description without exact names, only with trip duration and number
        # get username from database by session id
        result = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        username = result[0]["username"]

        results = db.execute("SELECT trip_length, COUNT(trip_length) FROM trips WHERE username = :username GROUP BY trip_length", username=username)
        print(results)

        return render_template("index.html", results=results)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", message="login get username error")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", message="login get password error")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology.html", message="invalid username/password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

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
            return render_template("apology.html", message="must provide a username")

        # Ensure password was submitted
        if not password:
            return render_template("apology.html", message="must provide a password")

        # Ensure confirmation for password was submitted
        if not request.form.get("confirmation"):
            return render_template("apology.html", message="must provide confirmation of the password")

        # Ensure password and confirmation are the same
        if request.form.get("confirmation") != password:
            return render_template("apology.html", message="password and confirmation are not the same")

        # Query database for username:
        rows = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))

        # Ensure username is not in the database
        if len(rows) != 0:
            return render_template("apology.html", message="Sorry, username is already in use")

        # INSERT into database
        db.execute("INSERT INTO users (username, hash) VALUES (:name, :password)", name=username, password=generate_password_hash(password))

        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        # Create local variables for username for database
        # get username from database by session id
        result = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        username = result[0]["username"]

        print(session["user_id"])
        print(username)


        # Create local variables for trip_name, trip_length and trip_description
        trip_name = request.form.get("trip_name")
        trip_length = request.form.get("trip_length")
        trip_description = request.form.get("trip_description")

        print(trip_name)
        print(trip_length)
        print(trip_description)

        if not trip_name:
            return render_template("apology.html", message="must provide name for the trip")

        if not trip_length:
            return render_template("apology.html", message="must provide length for the trip")

        if not trip_description:
            return render_template("apology.html", message="must provide at least a short trip description for the trip")

        db.execute("INSERT INTO trips (username, trip_name, trip_length, trip_description, selected, visited) VALUES (:username, :trip_name, :trip_length, :trip_description, :selected, :visited)", username=username, trip_name=trip_name, trip_length=trip_length, trip_description=trip_description, selected = 0, visited = 0)

        return render_template("upload.html", message= trip_name.title() + "Trip added!")
    else:
        return render_template("upload.html")

@app.route("/get_random", methods=["GET", "POST"])
@login_required
def get_random():
    result = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
    username = result[0]["username"]

    if request.method == "POST":
        decide = request.form.get('decide')
        print(str(decide))
        if decide == "Yes":
            # mark in database
            trip_name = request.form.get("trip_name")

            db.execute("UPDATE trips SET selected = 1 WHERE trip_name = :trip_name and username = :username", trip_name = trip_name, username=username)
            time.sleep(0.5)

            return redirect("http://30f8868c-172e-4e2e-89c3-f7d5d6f15a22-ide.cs50.xyz/maintenance")

        elif decide == "No":
            # Get a "list" of the available trip length
            trip_lengths = db.execute("SELECT trip_length FROM trips WHERE username = :username GROUP BY trip_length", username=username)
            print(trip_lengths)

            return render_template("get_random.html", results=trip_lengths)

        else:
            # Get username for the db query
            result = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
            username = result[0]["username"]

            # Get the selected length
            trip_length = request.form.get('length')

            print(trip_length + " is selected")

            # Get the available trips from database
            result = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username AND trip_length = :trip_length", username=username, trip_length=trip_length)
            # based on the numbers available generate a random number
            number = len(result)
            print("Total number: " + str(number))
            random_number = randint(0, number)

            print("Random number: " + str(random_number))

            # Present the n-th trip

            # Get a "list" of the available trip length
            results = db.execute("SELECT trip_length FROM trips WHERE username = :username GROUP BY trip_length", username=username)

            global_random_number = random_number
            global_results = results

            # Present the n-th trip
            return render_template("get_random.html", trip=result[random_number - 1], results=results)

    else:
        # Get a "list" of the available trip length
        trip_lengths = db.execute("SELECT trip_length FROM trips WHERE username = :username GROUP BY trip_length", username=username)
        print(trip_lengths)

        return render_template("get_random.html", results=trip_lengths)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/contact")
@login_required
def contact():
    """Contact page"""

    return render_template("contact.html")


@app.route("/maintenance", methods=["GET", "POST"])
@login_required
def maintenance():
    if request.method == "POST":
        # Get username for the db query
        result = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        username = result[0]["username"]

        if request.form.get('one_modification') == 'Modify':
            print("One modification branch")

            original_name = request.form.get("original_name")
            trip_name = request.form.get("trip_name")
            trip_length = request.form.get("trip_length")
            trip_description = request.form.get("trip_description")
            trip_visited = request.form.get("trip_visited")
            trip_selected = request.form.get("trip_selected")

            print("Original name" + original_name)
            print("Trip name: " + trip_name)
            print("Trip length: " + str(trip_length))
            print("Trip description: " + trip_description)
            print("Visited: " + str(trip_visited))
            print("Selected: " + str(trip_selected))

            if original_name == trip_name:
                # UPDATE in database
                print("One modification branch: the name of the trip was not modified.")
                db.execute("UPDATE trips SET trip_length= :trip_length, trip_description= :trip_description, visited= :trip_visited, selected= :trip_selected WHERE username= :username AND trip_name= :trip_name", username=username, trip_length=trip_length, trip_description=trip_description, trip_visited=trip_visited, trip_selected=trip_selected, trip_name=trip_name)

                selects = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username AND selected == 1 AND visited == 0", username=username)
                trips = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username ORDER BY trip_length ASC", username = username)
                visits = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username AND visited == 1 ORDER BY trip_length ASC, trip_name ASC", username=username)
                return render_template("maintenance.html", selects=selects, trips=trips, visits=visits)

            else:
                print("One modification branch: the name of the trip was modified.")
                #DELETE old entry, INSERT new one.
                db.execute("DELETE FROM trips WHERE username= :username AND trip_name= :trip_name", username=username, trip_name=original_name)
                db.execute("INSERT INTO trips (username, trip_name, trip_length, trip_description, selected, visited) VALUES (:username, :trip_name, :trip_length, :trip_description, :selected, :visited)", username=username, trip_name=trip_name, trip_length=trip_length, trip_description=trip_description, selected = trip_selected, visited = trip_visited)

                selects = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username AND selected == 1 AND visited == 0", username=username)
                trips = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username ORDER BY trip_length ASC", username = username)
                visits = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username AND visited ==1 ORDER BY trip_length ASC, trip_name ASC", username=username)

                return render_template("maintenance.html", selects=selects, trips=trips, visits=visits)
        elif request.form.get('one_modification') == 'Delete':
            print("One modification delete branch")
            original_name = request.form.get("original_name")
            db.execute("DELETE FROM trips WHERE username= :username AND trip_name= :trip_name", username=username, trip_name=original_name)
            selects = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username AND selected == 1 AND visited == 0", username=username)
            trips = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username ORDER BY trip_length ASC", username = username)
            visits = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username AND visited ==1 ORDER BY trip_length ASC, trip_name ASC", username=username)
            return render_template("maintenance.html", selects=selects, trips=trips, visits=visits)

        elif ((request.form.get('visited_modification') == "Modify" ) or (request.form.get("poll_modification") == "Modify") or (request.form.get('selected_modification') == "Modify")):
            print("visited_, poll_, selected_modification modify branch")
            trip_name = request.form.get("trip_name_to_modify")
            results = db.execute("SELECT * FROM trips WHERE username = :username AND trip_name = :trip_name", username=username, trip_name=trip_name)

            return render_template("maintenance.html", modifies=results)

        elif request.form.get("selected_modification") == "Mark as visited":
            print("selected modification 'Mark as visited' branch")
            trip_name = request.form.get("trip_name_to_modify")
            db.execute("UPDATE trips SET visited = 1 WHERE username = :username AND trip_name = :trip_name", username=username, trip_name=trip_name)

            selects = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username AND selected == 1 AND visited == 0", username=username)
            trips = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username ORDER BY trip_length ASC", username = username)
            visits = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username AND visited ==1 ORDER BY trip_length ASC, trip_name ASC", username=username)

            return render_template("maintenance.html", selects=selects, trips=trips, visits=visits)

        else:
            # not handled case.
            print("not handled case branch")
            return render_template("apology.html", message="Not handled case!")


    else:
        #TODO

        # Get all trips from the current user,
        #display the selected one first,
        #display all other ordered by the length of the trip,
        #and at last display the trips which are done

        result = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        username = result[0]["username"]
        selects = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username AND selected == 1 AND visited == 0", username=username)

        trips = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username ORDER BY trip_length ASC", username = username)

        visits = db.execute("SELECT trip_name, trip_length, trip_description FROM trips WHERE username = :username AND visited ==1 ORDER BY trip_length ASC, trip_name ASC", username=username)

        print(selects)
        print(trips)
        print(visits)

        return render_template("maintenance.html", selects=selects, trips=trips, visits=visits)