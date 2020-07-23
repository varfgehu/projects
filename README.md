HarvardX: CS50's Web Programming with Python and JavaScript

Final Project

I design a Web-based application to support my weight-loss attempt (and possibly help others'), by tracking the intake of calorie and nutritions through the days.
The User can upload foods to the database with nutrition details.
The User can assemble a proper meal with the uploaded foods, by setting the quantity for each food. With a help of a graph, the User can adjust each quantity for the selected foods to achieve the desired carb, protein, fat and calorie values.

Justification:
During implementetion Django object models to create database structure, JavaScript to modify html table real-time and filter list, CanvasJS to render graphs.
The problems and solutions were more complex than any of the lecture samples or projects.

Detailed Description:

home.html
After loging in the User is redirected to the Home page.
All personal and latest measurement data ( weight, BMI value, Body Fat % and Body Water %) are shown which are necessary for the optimal calorie intake calculation, which are also displayed. These data are loaded from the database or calculated based on these data.
In a following section the User can add his or her latest measurements, which are loaded to the database.
There is also a graph to review the progress. The User can zoom and search in the graph as well. The graph is implented in JavaScript, using CanvasJS, and based on the huge table below. It is loaded from the database and also useful for further inspections.

set_personal_info.html
On the Set personal info the User can set some Personal data for the optimal calorie calculation. It is also possible to set the desired nutrition distribution.

add_meal_defined.html
The main functionality is implemented in Prepare Meal page.
The User can select a date and the exact meal, which he or she would like to prepare a meal for with the optimal levels of nutritions.
The User can select foods from the database, set the quantity of it and add to the selected meal. The meals are stored in the database.
The added items are loaded to a table, displaying the nutritions and calorie amounts corresponding to the given amount for each food. The amounts still can be changed via input field in the table. The modifications are loaded to the table instatly with JavaScript implementation. A graph is also implemented, it displays the calculated optimal ammount of each nutrition and the sum of nutritions and calorie of the selected foods. In this way the User can easily assemble a proper meal with the optimal amounts of nutritions and calorie. The graph also adapts the the change of the table, also implemented by CanvasJS.

maintain_food_data.html
On Maintain Food Data page a list of links are generated for each food item, to modify the nutrition and calorie values. The list can be filtered via an input field, implemented with JavaScript. It is also possible to add new Food to the database.

food.html
It is a base for rendering a page to modify any of the foods' mutritions and calorie values.
URL: food/<int:id>

login.html
Allows the user to login to the application.

register.html
Allows the user to create a registration.

base.html
Template for the html pages.

helper.py, access_measurement.py, access_personal.py
Experimenting with extracting functions from the views.py to be more organized.

tests.py
Experimenting with with testing with unittest and selenium

ci.yml
yml file to experiment with CI in github

Procfile
Experimenting with deployment to Heroku

requirements.txt
Experimenting with deployment to Heroku
