import os

from flask import Flask, session, jsonify, render_template, request, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room

from collections import deque

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

# Forget any users
usersLoggedIn.clear()



@app.route("/")
@login_required
def index():
    print("Logged in users:")
    print(usersLoggedIn)

    print("Existing Channels:")
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
    try:
        usersLoggedIn.remove(session['username'])
    except ValueError:
        pass

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

        channel_messages[new_channel] = deque(maxlen=100)

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

    print(channel_messages[channel_name])

    if request.method == "POST":
        print("channel/" + channel_name + " POST")
    else:
        return render_template("channel.html", messages = channel_messages[channel_name])

@socketio.on("joined")
def joined():
    """
    Notify other users of joining a channel(room)
    """

    channel = session["channel_entered"]

    join_room(channel)

    join_message = '[-- ' + session['username'] + ' has joined the channel --]\n'

    emit('status_update', {
        'user': session['username'],
        'message': join_message,
        'channel': channel},
        room = channel)

    channel_messages[session['channel_entered']].append(join_message)

@socketio.on("left")
def leave():
    """
    Notify other users of joining a channel(room)
    """
    channel = session["channel_entered"]

    leave_room(channel)

    left_message = '[-- ' + session['username'] + ' has left the channel --]\n'

    emit('status_update', {
        'user': session['username'],
        'message': left_message},
        room = channel)

    channel_messages[session['channel_entered']].append(left_message)

@socketio.on("submit message")
def message(data):
    print('"submit message" detected')
    print(data)

    if len(channel_messages[session['channel_entered']]) > 100:
        print("max number of messages reached")
        leave_room(session["channel_entered"])
        return render_template("apology.html", message="Sorry, you have exceeded the 100 messages/channel limit. You can create a new channel.")

    print(channel_messages[session['channel_entered']])

    processed_message = session['username'] + ": " + data["new_message"] + "\n"
    channel_messages[session['channel_entered']].append(processed_message)

    emit('announced message', {
        'new_message': processed_message
        }, room = session['channel_entered'] )
