from flask import Flask, render_template, request
import requests as rq
import fpl_functions as fpl
import pandas as pd
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#supress warnings
warnings.filterwarnings("ignore")

#Creating the app
app = Flask(__name__)
# api to the FPL data's
api = 'https://fantasy.premierleague.com/api/bootstrap-static/#/'

# live game week api = https://fantasy.premierleague.com/api/event/(gwnumber)/live/
# points_api per player id: https://fantasy.premierleague.com/api/element-summary/


# Converting the api to a database/dataframe fro mdata from the API 
data = rq.get(api)
database = data.json()
main_df = pd.DataFrame(database['elements'])

# Sliiming down the dataframe to the only values I require
slim_main_df = main_df[['id', 'web_name', 'element_type', 'team', 'now_cost', 'total_points']]
slim_main_df.rename(columns={'element_type' : 'position', 'web_name' : 'name', 'now_cost' : 'price'}, inplace = True)

# Altering certain columns to more readable names
for i in range(len(slim_main_df['position'])):
    slim_main_df['position'][i] = fpl.position(slim_main_df['position'][i])

for j in range(len(slim_main_df['team'])):
    slim_main_df['team'][j] = fpl.find_team(slim_main_df['team'][j], database)

# Converting cost to correct value
slim_main_df['price'] = slim_main_df.loc[:, ('price')]/10.0

#getting the current gameweek
gw = pd.DataFrame(database['events'])
gws = gw[['id', 'finished']]
for week, ids in gws.iterrows():
    if ids['finished'] != True:
        current_gw = ids['id']
        break

player_list, teams = fpl.get_player_list(database)
print(player_list)

# Initial figure on page (empty)
player_id = 10
gw_points, total_points = fpl.player_weekPoints(player_id)
x_axis = [x for x in range(1, len(total_points) + 1)]
total_points = [0] * len(gw_points)
print(len(x_axis))
print(len(total_points))
plt.bar(x_axis, total_points)
plt.ylabel("Total Points")
plt.xlabel("Gameweek")
plt.savefig('c:/Users/chira/Documents/Coding/FPL/web/static/plot.jpg')


@app.route("/")
def index():
    return render_template("index.html", player_list = player_list, teams = teams)

@app.route('/', methods=['POST'])
def my_form_post():
    #Obtain user's inputted player
    player_name = request.form['players']
    player_id = fpl.find_player_id(database, player_name)


    gw_points, total_points = fpl.player_weekPoints(player_id)
    x_axis = range(1, len(total_points))
    plt.close()
    x_axis = [x for x in range(1, len(total_points) + 1)]
    plt.bar(x_axis, gw_points)
    plt.ylabel("Total Points")
    plt.xlabel("Gameweek")
    if request.form.get("addOn") != None:
        plt.plot(x_axis, total_points)
    plt.savefig('c:/Users/chira/Documents/Coding/FPL/web/static/plot.jpg')
    print(player_id)
    
    return render_template("index.html", player_list = player_list, teams = teams)

@app.route("/dbase.html")
def dbase():
    return render_template("dbase.html", tables = [slim_main_df.to_html(classes='data')], titles=slim_main_df.columns.values)


if __name__ == '__main__':
    app.run(host='0.0.0.0')