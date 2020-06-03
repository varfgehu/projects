# Project 2

Web Programming with Python and JavaScript

Overview
In this project, you’ll build an online messaging service using Flask, similar in spirit to Slack. Users will be able to sign into your site with a display name, create channels (i.e. chatrooms) to communicate in, as well as see and join existing channels. Once a channel is selected, users will be able to send and receive messages with one another in real time.

templates/apology.html
Error handling is implemented in it. 

templates/channel.html:
The HTML page is created with the main 4 structures in it:
- textare for received messages,
- input field for messages to send
- button to send the message
- button to leave channel
Also channel.js javascript is "included"

templates/index.html:
The HTML page is created to:
- create new channel for the user (input field and button)
- unordered list of links of the existing channels (if any)

templates/layout.html
Creating the a template for the html pages.

templates/login.html
The HTML page is created to:
- assign a username to the app user.

static/channel.js:
Script runs when a user opens a channel.
When the page is loaded:
- emit a 'join' signal
- add event listener to "Leave Channel" button, if so: emit 'left' signal, remove 'current_channel' from local storage
- add event listener to 'Channels' button on the nav bar, creating a proper way to leave the channel the same way as with the button
- add event listener to 'new_message' input field, to send message with pressing 'Enter'
- scroll down in the textarea to the bottom.
Catch 'status_update' emit from server side:
- add text to 'chat_area' from received data
- scroll down in the textarea to the bottom
- save 'current_channel' to local storage.

static/channels.js:
Script runs when a user loads the index page.
If the 'current_channel'  exists in local storage and stores relevant data, load the channel page.

static/login.js:
if login page is loaded, remove 'current_channel'from local storage.

application.py:
imports, app initialization
Creating global variables to store existing channels, logged in usernames, channel messages which is a dictionary with deques.
Route functions:
index: renders index.html, giving the list of existing channels to it.
login: GET request: renders login.html; POST request: if username is valid and not already taken, redirects user to index page
logout: removes username from the username list, clears session.
create: POST request: get the new channel name from html form (new_channel). If channel is truly new, it is appended to the existing channel list and creates a max 100 length deque in the channel messages dictionary. Then redirects user to channel/#channel_name page
channel/#channel_name:
Saves channel name to session and renders channel page, give the page the messages in attribute.

Catching socket signals:
joined: call join_room in  flask_socketio to connect user to the channel (or room). Create a message that a user has joined the channel. Emit it as 'status_update' to populate the textarea in channels.html. Add message to channel_messages to store it.

left: call leve_room in flask_socketio to disconnect user from the channel (or room). Create a message that a suer has left the channel. Emit it as 'status_update' to populate the textarea in channel.html. Add message to channel messages to store it.

submit_message:
If the 100 number of messages is not reached, prepare the message that will be inserted to the textarea.













