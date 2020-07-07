HarvardX: CS50W. CS50's Web Programming with Python and JavaScript

Final Project

I design a Web-based application to support my weight-loss attempt (and possibly help others'), by tracking the intake of calorie and nutritions.

Naturaly, registration, login and logout are implemented with the authenticate, login, logout functions in django.contrib.auth .

After loging in the User is redirected to the home page.
All personal and and latest measurement data ( weight, BMI value, Body Fat % and Body Water %) are shown which are necessary for the optimal calorie intake calculation, which are also displayed. These data are loaded from the database or calculated based on these data.
In a following section the User can add his or her latest measurements, which are loaded to the database.
There is also a graph to review the progress. The User can zoom and search in the graph as well. The graph is implented in JavaScript, using CanvasJS, and based on the huge table below. It is loaded from the database and also useful for further inspections.

On the Set personal info the User can set some Personal data for the optimal calorie calculation. It is also possible to set the desired nutrition distribution.

The main functionality is implemented in Prepare Meal page.
The User can select a date and the exact meal, which he or she would like to prepare a meal for with the optimal levels of nutritions. The calculated optimal daily calorie intake is distributed evenly between 3 large (breakfast, lunch and dinner with 1/4 of the daily calorie for each) and 2 small (2 snacks with 1/8 of the daily calorie for each) meals. The User can select foods from the database, set the amount of it and add to the selected meal. The meals are stored in the database. The added items are loaded to a table, displaying the nutritions and calorie amounts corresponding to the given amount for each food. The amounts still can be changed via input field in the table. The modifications are loaded to the table instatly with JavaScript implementation. A graph is also implemented, it displays the calculated optimal ammount of each nutrition and the sum of nutritions and calorie of the selected foods. In this way the User can easily prepare a proper meal with the optimal amounts of nutritions and calorie. The graph also adapts the the change of the preparation table, also implemented by CanvasJS.

On Maintain Food Data page a list of links are generated for each food item, to modify the nutrition and calorie values. The list can be filtered via an input field, implemented with JavaScript. It is also possible to add new Food to the database.
