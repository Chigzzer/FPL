import requests
import pandas as pd
import numpy as np
import fpl_functions as fpl
import interface
import warnings


#supress warnings
warnings.filterwarnings("ignore")

# Obtain the user's team ID and the gameweek
# Obtaining the current gameweek input 
current_gw = input("What gameweek? ")
"""
Posibly add a code here to check current if entered 0 and go to current event number by looking at history api
"""
team_id = input("What is your id? ")

# URL for the overall database and the user's team
id_url = 'https://fantasy.premierleague.com/api/bootstrap-static/#/'
my_team_url = 'https://fantasy.premierleague.com/api/entry/' + team_id + '/event/' + \
    str(current_gw) + '/picks/'

my_team = requests.get(my_team_url)
r = requests.get(id_url)

#Create database for all the platers in the system
json_database = r.json()

 # Obtaining data about your team1
json_team = my_team.json()
user_team_history = json_team['entry_history']
picks = json_team['picks']

# Looking at the overall database of the system
# creating datarame for every player
main_df = pd.DataFrame(json_database['elements'])
#print(main_df.keys())
slim_main_df = main_df[['web_name', 'element_type', 'team', 'now_cost', 'total_points']]
# Renaming headers
slim_main_df.rename(columns={'element_type' : 'position', 'web_name' : 'name', 'now_cost' : 'price'}, inplace = True)

# converting position and team id to the actual name.
for i in range(len(slim_main_df['position'])):
    slim_main_df['position'][i] = fpl.position(slim_main_df['position'][i])

for j in range(len(slim_main_df['team'])):
    slim_main_df['team'][j] = fpl.find_team(slim_main_df['team'][j], json_database)

# Converting cost to correct value
slim_main_df['price'] = slim_main_df.loc[:, ('price')]/10.0

interface.main_menu(slim_main_df,main_df)


