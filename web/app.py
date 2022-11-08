from flask import Flask, render_template, request
import requests as rq
import fpl_functions as fpl
import pandas as pd

app = Flask(__name__)

api = 'https://fantasy.premierleague.com/api/bootstrap-static/#/'

# points_api = https://fantasy.premierleague.com/api/event/(gwnumber)/live/
# points_api per player id: https://fantasy.premierleague.com/api/element-summary/'player_id'/


data = rq.get(api)
database = data.json()
main_df = pd.DataFrame(database['elements'])
slim_main_df = main_df[['id', 'web_name', 'element_type', 'team', 'now_cost', 'total_points']]
slim_main_df.rename(columns={'element_type' : 'position', 'web_name' : 'name', 'now_cost' : 'price'}, inplace = True)
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


#Trying to get the points each player has each gameweek
points_api = 'https://fantasy.premierleague.com/api/event/1/live/'
points_data = rq.get(points_api)
points_db = points_data.json()
points_df = pd.DataFrame(points_db['elements'])
points_df_id = points_df['id'] #gets player id

#Trying to get table of the players points
points_df_points = points_df['stats']
print(points_df_points)

#points_df_points = points_df['stats']['total_points']
#frames = [points_df_id, points_df_points]
#table = pd.concat(frames)
#display(table)





@app.route("/")
def index():
    return render_template("index.html", tables = [slim_main_df.to_html(classes='data')], titles=slim_main_df.columns.values)

@app.route("/dbase.html")
def dbase():
    return render_template("index.html", tables = [slim_main_df.to_html(classes='data')], titles=slim_main_df.columns.values)


if __name__ == '__main__':
    app.run(host='0.0.0.0')