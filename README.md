# Project: FPL Points Tracker
### Author: Chiraag Chandarana
### Country: United Kingdom
## Video Demo: https://youtu.be/whYjBjjGB_M
## Description:
This is a simple web application that uses a Python backend (flask) and HTML, CSS and a bit of Javascript for the font end.

This project was done due to my interest in Football and the Premier League. Every year I play the Fantasy Premier League Football (FPL) and one of the issues I keep facing is when choosing players and looking at their points. Currently the website tells you their total points at a glance. Viewing their points every game week is available on the main site, but in numerical form. Producing this application allows me to see the player's points each game week in a graphical manner. This would allow me to see if the player is in form, getting high points recently, or whether majority of his points is from earlier in the season. I have produced this application by gathering data from the FPL API and analysing it using the library matplotlib.

### File Structure
This application has two python files: app.py and fpl_functions.py. The former is the backend application that runs the website via the framework Flask. The later contains sup[porting functions I have created to help obtain data from the API and analyse it. The website application has two pages: Home and Team.

The Home page is the initial page which lists all the player's available in the game, grouped together by their team. The user can select the player he wants to plot onto the graph and once he clicks submit the graph will be populated with that player's points. More than one player can be plotted by plotting one player and than submitting another without clicking reset.

The Team page is similar to the home page, except the user has to provide their Team ID first; so the application can gather the players they picked. Once the user has entered his team ID, a user guide is available on how to get the team ID via click of a button, a page similar to the home screen will pop up with only player's from their team listed. 

## Future Ideas
This is a project which can be worked on and continuously updated. Some ideas that could be implemented is:
* Allow user to select if they want to see the data via a line graph vs a bar chart.
* Add a page where the user can plan their team or change their player's to see how many points they could have had if they made that transfer.
* Have the plot colour coordinated to show how the points gained that game week were by: a goal, assist, e.g. 

