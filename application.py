import os, json

from flask import Flask, session, request, render_template, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash
import requests

from helper import login_required

#goodreads API key #lVk1cdNsPkwrSfEpGwtKg#

app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    Search:
    Once a user has logged in, they should be taken to a page
    where they can search for a book. Users should be able to type in the ISBN
    number of a book, the title of a book, or the author of a book.
    After performing the search, your website should display
    a list of possible matching results, or some sort of message
    if there were no matches.
    If the user typed in only part of a title, ISBN, or author name,
    your search page should find matches for those as well!
    """

    if request.method == "POST":
        print("index.html POST")

    else:
        print("index.html GET")
        return render_template("index.html")

@app.route("/books", methods=["POST"])
@login_required
def books():
    print("book.html POST")
    # Create local variables for isbn, title, author
    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")

    print(isbn)
    print(title)
    print(author)

    # If isbn was filled, search based on isbn, give the result to render_template
    if isbn:
        search_for = "%{}%".format(isbn)
        print(search_for)
        books = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn", {"isbn": search_for}).fetchall()
        if books:
            return render_template("books.html", books = books)
    # If title was filled, search based on title, give the result to render_template
    if title:
        search_for = "%{}%".format(title)
        print(search_for)
        books = db.execute("SELECT * FROM books WHERE title LIKE :title", {"title": search_for}).fetchall()
        if books:
            return render_template("books.html", books = books)

    # If author was filled, search based on author, give the result to render_template
    if author:
        search_for = "%{}%".format(author)
        print(search_for)
        books = db.execute("SELECT * FROM books WHERE author LIKE :author", {"author": search_for}).fetchall()
        if books:
            return render_template("books.html", books = books)

    return render_template("apology.html", message = "Nothing is found based on your search information!")

@app.route("/book/<int:book_id>", methods=["POST", "GET"])
@login_required
def book(book_id):
    if request.method == "POST":
        # Create local variables for data
        rating = request.form.get("rating")
        review = request.form.get("review")

        results = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id": session["user_id"], "book_id": book_id})

        if results.rowcount == 1:
            return redirect("/book/" + str(book_id))

        rating = int(rating)

        db.execute("INSERT INTO reviews (user_id, book_id, text, rating) VALUES (:user_id, :book_id, :review, :rating)", \
                    {"user_id":session["user_id"], "book_id": book_id, "review": review, "rating": rating})
        db.commit()

        return redirect("/book/" + str(book_id))

    else:
        print("Book id: " + str(book_id))
        results = db.execute("SELECT isbn, title, author, year FROM books WHERE id = :book_id", {"book_id": book_id}).fetchall()

        isbn = results[0]["isbn"]
        goodreads_key = os.getenv("GOODREADS_KEY")


        # API request to goodreads.com
        goodreads_response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": goodreads_key, "isbns": isbn})
        print(goodreads_response.json())


        # Make response JSON format
        goodreads_json = goodreads_response.json()
        goodreads_json = goodreads_json['books'][0]

        reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id}).fetchall()
        own_review = db.execute("SELECT * FROM reviews WHERE book_id = :book_id AND user_id = :user_id", {"book_id": book_id, "user_id": session["user_id"]}).fetchone()

        return render_template("book.html", results=results, goodreads_json=goodreads_json, reviews=reviews, own_review=own_review)


@app.route("/api/<isbn>")
def api(isbn):
    """Return details about a book based on isbn"""
    print(type(isbn))
    print(isbn)
    #results = db.execute("SELECT title, author, year, isbn, COUNT(reviews.id) as review_count, AVG(reviews.rating) as average_score FROM books INNER JOIN reviews ON books.id = reviews.book_id WHERE isbn = :isbn GROUP BY title, author, year, isbn", {"isbn": isbn})
    results = db.execute("SELECT title, author, year, isbn, COUNT(reviews.id) as review_count, AVG(reviews.rating) as average_score FROM books INNER JOIN reviews ON books.id = reviews.book_id WHERE books.isbn = :isbn GROUP BY title, author, year, isbn", {"isbn": isbn})

    print(results.rowcount)
    # Check for error
    if results.rowcount != 1:
        return jsonify({"error_message": "Invalid book ISBN number!", "error_code": 404}), 404

    result = results.fetchone()

    print(result)

    result_dict = dict(result.items())
    result_dict['year'] = int(result_dict['year'])
    result_dict['average_score'] = float('%.2f'%(result_dict['average_score']))


    return jsonify(result_dict)

    #return jsonify({\
    #        "title": ,
    #        "author": ,
    #        "year": ,
    #        "isbn": isbn,
    #        "review_count": ,
    #        "average_score:":
    #})

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Registration:
    Users should be able to register for your website,
    providing (at minimum) a username and password.
    """
    if request.method == "POST":
        # Create local variables for username and password and confirm password
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        print(username)
        print(password)
        print(confirm)

        # Check if all inputs are filled in
        if username == "":
            return render_template("apology.html", message="Please fill username field!")

        if password == "":
            return render_template("apology.html", message="Please fill password field!")

        if confirm == "":
            return render_template("apology.html", message="Please fill second password field!")

        # Check if password and confirm are the same
        if password != confirm:
            return render_template("apology.html", message="Password and second password must be the same")

        # Check for existing username
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount != 0:
            return render_template("apology.html", message="username is taken!")

        # Everything look fine, insert new user to users database
        print(generate_password_hash(password))
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": generate_password_hash(password)})
        db.commit()

        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login:
    Users, once registered, should be able to log in to your website
    with their username and password.
    """
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Create local variables for username and password and confirm password
        username = request.form.get("username")
        password = request.form.get("password")

        print(username)
        print(password)

        # Make sure username was submitted
        if not username:
            return render_template("apology.html", message="Please fill username field!")

        # Make sure password was submitted
        if not password:
            return render_template("apology.html", message="Please fill password field!")

        # Make sure username is in the database with the correct password check_password_hash
        rows = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchall()
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            return render_template("apology.html", message="invalid username/password")

        # Remember the user in sessionmaker
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """
    Logout:
    Logged in users should be able to log out of the site.
    """
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")















def login_required():
    if session.get("user_id") is None:
        return redirect("/login")
