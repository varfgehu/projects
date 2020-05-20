# Project 1

Web Programming with Python and JavaScript
Project 1: Book

Necessary API keys from environmental variables:
DATABASE_URL
GOODREAD_KEY
Please set them before running the web application.

Page descriptions:

/register
A successful registration has the following requirements:
- all 3 input fields should be filled in
- the selected username should not be found in the database as a Username
- the password and the password confirmation should be identical
The user will be notified if any of the input fields misses any requirements

/login
A successful log in has the following requirements:
- all 2 input fields should be filled in
- the entered username should be present in the database
- the calculated password hash should be present in the database with the entered Username
After a successful log in, the user id is saved to session

/logout
After a successful log out, the user id is cleared from session

/index
The user can search in the database of the website by a frcation or the full ISBN number
or Author or Title.
The user should use only one input field. Any missuse will cause undifined behavoiur for the user.
(The applicatoin will user the first filled input filed for the search.)
The rules of searching can be found on the index page.
By pressing Search button the user will be redirected to books page with the findings.

/books
The user will be redirected to this page with the findings of his/her search.
The following information will be shown of the found book(s): author, title, book cover
and a link to the detailed book page.

/book/<int:book_id>
Detailed book page with the following information:
Large size book cover, author, title, year if publication, ISBN number.
Rating and review number for Goodread website. Link to the webpage of the book on Goodread's website.
The user has the opportunity the leave a review and a reting for each book, but only one for each book.
If the logged in user has already left a review, the user review field will notify the user, other case the user can leave a review through a drop-down list and a textarea.
If other user reviews are exist, the user can found in in the last section of the page.

/api/<isbn>

If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score.
