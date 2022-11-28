from flask import Flask, render_template, request, redirect, flash
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



# Converting the api to a database/dataframe fro mdata from the API 
data = rq.get(api)
database = data.json()
mainDF = pd.DataFrame(database['elements'])

# Sliiming down the dataframe to the only values I require
slimMainDf = mainDF[['id', 'web_name', 'element_type', 'team', 'now_cost', 'total_points']]
slimMainDf.rename(columns={'element_type' : 'position', 'web_name' : 'name', 'now_cost' : 'price'}, inplace = True)

# Altering certain columns to more readable names
for i in range(len(slimMainDf['position'])):
    slimMainDf['position'][i] = fpl.position(slimMainDf['position'][i])

for j in range(len(slimMainDf['team'])):
    slimMainDf['team'][j] = fpl.findTeam(slimMainDf['team'][j], database)

# Converting cost to correct value
slimMainDf['price'] = slimMainDf.loc[:, ('price')]/10.0

#getting the current gameweek
gw = pd.DataFrame(database['events'])
gws = gw[['id', 'finished']]
for week, ids in gws.iterrows():
    if ids['finished'] != True:
        currentGw = ids['id']
        break

playerList, teams = fpl.getPlayerList(database)
# Initial figure on page (empty)


@app.route("/")
def index():
    plt.close()
    playerId = 10
    gwPoints, totalPoints = fpl.playerWeekPoints(playerId)
    x_axis = [x for x in range(1, len(totalPoints) + 1)]
    totalPoints = [0] * len(gwPoints)
    plt.bar(x_axis, totalPoints)
    plt.ylabel("Total Points")
    plt.xlabel("Gameweek")
    print(totalPoints)
    plt.savefig('c:/Users/chira/Documents/Coding/FPL/static/plot.jpg')
    return render_template("index.html", playerList = playerList, teams = teams)

@app.route('/', methods=['POST'])
def homeGraph():
    #Obtain user's inputted player
    if not request.form.get('players'):
        return redirect('/')
    playerName = request.form.get('players')
    playerId = fpl.findPlayerId(database, playerName)
    gwPoints, totalPoints = fpl.playerWeekPoints(playerId)
    x_axis = [x for x in range(1, len(totalPoints) + 1)]
    plt.bar(x_axis, gwPoints, width=0.2, label=playerName)
    plt.ylabel("Total Points")
    plt.xlabel("Gameweek")
    plt.legend()
    if request.form.get("addOn") != None:
        plt.plot(x_axis, totalPoints, label=playerName)
        plt.legend()
    plt.savefig('c:/Users/chira/Documents/Coding/FPL/static/plot.jpg')    
    return render_template("index.html", playerList = playerList, teams = teams)

@app.route("/team", methods=['GET', 'POST'])
def team():
    return render_template("team.html")



@app.route("/teamSelect", methods=['GET','POST'])
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
        str(currentGw - 1) + '/picks/'
    teamData = rq.get(teamUrl)
    teamDatabase = teamData.json()

    # Checks to confirm if the team id provides a valid response
    if 'detail' in teamDatabase:
        return redirect("/team")
    teamPlayers = fpl.getTeamPlayers(teamDatabase, database)  
    plt.close()
    playerId = 10
    gwPoints, totalPoints = fpl.playerWeekPoints(playerId)
    x_axis = [x for x in range(1, len(totalPoints) + 1)]
    totalPoints = [0] * len(gwPoints)
    plt.bar(x_axis, totalPoints)
    plt.ylabel("Total Points")
    plt.xlabel("Gameweek")
    plt.savefig('c:/Users/chira/Documents/Coding/FPL/static/plot.jpg')
    return render_template("teamgraph.html", playerList = teamPlayers, teamID = teamID)

@app.route("/teamSelected", methods=['POST'])
def teamGraph():
    # Getting the team's players
    if not request.form.get('players'):
        return redirect('/teamSelected')

    teamID = request.form.get('teamID')
    teamUrl = 'https://fantasy.premierleague.com/api/entry/' + teamID + '/event/' + \
                 str(currentGw - 1) + '/picks/'
    teamData = rq.get(teamUrl)
    teamDatabase = teamData.json()
    teamPlayers = fpl.getTeamPlayers(teamDatabase, database)  
    playerName = request.form.get('players')
    playerId = fpl.findPlayerId(database, playerName)
    # Populate the graph with the player's points
    gwPoints, totalPoints = fpl.playerWeekPoints(playerId)
    x_axis = range(1, len(totalPoints))
    x_axis = [x for x in range(1, len(totalPoints) + 1)]
    plt.bar(x_axis, gwPoints, width=0.2, label=playerName)
    plt.ylabel("Total Points")
    plt.xlabel("Gameweek")
    plt.legend()
    if request.form.get("addOn") != None:
        plt.plot(x_axis, totalPoints, label=playerName)
        plt.legend()
    plt.savefig('c:/Users/chira/Documents/Coding/FPL/static/plot.jpg')    
    return render_template("teamgraph.html", playerList = teamPlayers, teamID = teamID)


if __name__ == '__main__':
    app.run(host='0.0.0.0')