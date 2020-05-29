import os

from flask import Flask, session, jsonify, render_template, request, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit

from helpers import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Store existing channels
existingChannels = []

# Store logged in users
usersLoggedIn = []

# Store messages for each channel
channel_messages = dict()

@app.route("/")
@login_required
def index():
    print(existingChannels)
    return render_template("index.html", channels=existingChannels)

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Forget any users
    session.clear()

    username = request.form.get("username")

    if request.method == "POST":
        print("login POST detected")
        if len(username) < 1 or username is '':
            return render_template("apology.html", message="username can not be empty")

        if username in usersLoggedIn:
            return render_template("apology.html", message="username has already taken!")

        usersLoggedIn.append(username)

        session['username'] = username
        print("Username: " + username)

        # Remember the user session on a cookie if the browser is closed
        #session.permanent = True

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """
    Logout:
    Logged in users should be able to log out of the site.
    """

    # Remove username from the taken list
    usersLoggedIn.remove(session['username'])

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """
    Create new channel, add to local list and redirect user to index
    """

    if request.method == "POST":
        new_channel = request.form.get("new_channel")

        if new_channel in existingChannels:
            return render_template("apology.html", message="Channel already exists!")

        existingChannels.append(new_channel)
        print(existingChannels)

        channel_messages[new_channel] = []

        return redirect("/channel/" + new_channel)
    else:
        return render_template("apology.html", message="create GET request branch")


@app.route("/channel/<channel_name>", methods=["GET", "POST"])
@login_required
def channel(channel_name):
    """
    Open channel page, to read and send messages
    """
    session['channel_entered'] = channel_name

    if request.method == "POST":
        print("channel/" + channel_name + " POST")
    else:
        return render_template("channel.html", messages = channel_messages[channel_name])
