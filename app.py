from flask import Flask, render_template, request, redirect
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
app.config['DEBUG'] = True
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
# Initial figure on page (empty)


@app.route("/")
def index():
    plt.close()
    player_id = 10
    gw_points, total_points = fpl.player_weekPoints(player_id)
    x_axis = [x for x in range(1, len(total_points) + 1)]
    total_points = [0] * len(gw_points)
    plt.bar(x_axis, total_points)
    plt.ylabel("Total Points")
    plt.xlabel("Gameweek")
    print(total_points)
    plt.savefig('c:/Users/chira/Documents/Coding/FPL/static/plot.jpg')
    return render_template("index.html", player_list = player_list, teams = teams)

@app.route('/', methods=['POST'])
def my_form_post():
    #Obtain user's inputted player
    if not request.form.get['players']:
        return redirect('/')
    player_name = request.form['players']
    player_id = fpl.find_player_id(database, player_name)
    gw_points, total_points = fpl.player_weekPoints(player_id)
    x_axis = range(1, len(total_points))
    x_axis = [x for x in range(1, len(total_points) + 1)]
    plt.bar(x_axis, gw_points, width=0.2, label=player_name)
    plt.ylabel("Total Points")
    plt.xlabel("Gameweek")
    plt.legend()
    if request.form.get("addOn") != None:
        plt.plot(x_axis, total_points)
        plt.legend()
    plt.savefig('c:/Users/chira/Documents/Coding/FPL/static/plot.jpg')    
    return render_template("index.html", player_list = player_list, teams = teams)

@app.route("/dbase.html")
def dbase():
    return render_template("dbase.html", tables = [slim_main_df.to_html(classes='data')], titles=slim_main_df.columns.values)



@app.route("/team", methods=['GET', 'POST'])
def team():
    return render_template("team.html")



@app.route("/teamSelect", methods=['POST'])
def teamSelect():
    # Checks if an ID has been submitted
    if not request.form.get("teamID"):
        return redirect("/team")
    # Checks to see if ID is a number as required
    try:
        int(float(request.form.get("teamID")))
    except ValueError:
        return redirect("/team")
    
    # Obtains the team id from form and then obtains the player's in that selected team
    teamID = request.form.get('teamID')
    teamUrl = 'https://fantasy.premierleague.com/api/entry/' + teamID + '/event/' + \
        str(current_gw - 1) + '/picks/'
    teamData = rq.get(teamUrl)
    teamDatabase = teamData.json()

    # Checks to confirm if the team id provides a valid response
    if 'detail' in teamDatabase:
        return redirect("/team")
    teamPlayers = fpl.getTeamPlayers(teamDatabase, database)  
    plt.close()
    player_id = 10
    gw_points, total_points = fpl.player_weekPoints(player_id)
    x_axis = [x for x in range(1, len(total_points) + 1)]
    total_points = [0] * len(gw_points)
    plt.bar(x_axis, total_points)
    plt.ylabel("Total Points")
    plt.xlabel("Gameweek")
    plt.savefig('c:/Users/chira/Documents/Coding/FPL/static/plot.jpg')
    return render_template("teamgraph.html", player_list = teamPlayers, teamID = teamID)

@app.route("/teamSelected", methods=['POST'])
def teamGraph():
    # Getting the team's players
    teamID = request.form.get('teamID')
    teamUrl = 'https://fantasy.premierleague.com/api/entry/' + teamID + '/event/' + \
                 str(current_gw - 1) + '/picks/'
    teamData = rq.get(teamUrl)
    teamDatabase = teamData.json()
    teamPlayers = fpl.getTeamPlayers(teamDatabase, database)  
    player_name = request.form['players']
    player_id = fpl.find_player_id(database, player_name)
    # Populate the graph with the player's points
    gw_points, total_points = fpl.player_weekPoints(player_id)
    x_axis = range(1, len(total_points))
    x_axis = [x for x in range(1, len(total_points) + 1)]
    plt.bar(x_axis, gw_points, width=0.2, label=player_name)
    plt.ylabel("Total Points")
    plt.xlabel("Gameweek")
    plt.legend()
    if request.form.get("addOn") != None:
        plt.plot(x_axis, total_points)
        plt.legend()
    plt.savefig('c:/Users/chira/Documents/Coding/FPL/static/plot.jpg')    
    return render_template("teamgraph.html", player_list = teamPlayers, teamID = teamID)


if __name__ == '__main__':
    app.run(host='0.0.0.0')