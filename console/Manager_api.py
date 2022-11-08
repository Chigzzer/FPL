import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Created for initial draft of the manager's layout


# Obtaining the current gameweek input 
current_gw = input("What gameweek? ")
"""
Posibly add a code here to check current if entered 0 and go to current event number by looking at history api
"""
team_id = input("What is your id? ")
id_url = 'https://fantasy.premierleague.com/api/bootstrap-static/#/'
my_team_url = 'https://fantasy.premierleague.com/api/entry/' + team_id + '/event/' + \
    str(current_gw) + '/picks/'

my_team = requests.get(my_team_url)
r = requests.get(id_url)

json_database = r.json()




    
 # Obtaining data about your team1
json_team = my_team.json()
team_history = json_team['entry_history']
picks = json_team['picks']


# Looking at the overall database of the system
print("KEYS:")
player = find_player_code(json_database, "Salah")
print(player)

# print(json_database['elements'][0]['code'])
id_df = pd.DataFrame(json_database['elements'])
print(id_df.keys())
elements_types_df = pd.DataFrame(json_database['element_types'])
print(elements_types_df)
slim_id_df = id_df[['second_name', 'id', 'now_cost']]
slim_id_df['position'] = slim_id_df.element_type.map(elements_types_df.set_index('id').singular_name)
#print(slim_id_df)
picks_df = pd.DataFrame(picks)
#print('here:', id_df.loc[id_df.id == picks_df.element[1], 'second_name'])

names = []
price = []
pos = []
for i in range(len(picks_df.element)):
    pri_val = id_df.loc[id_df.id == picks_df.element[i], 'now_cost']
    val = id_df.loc[id_df.id == picks_df.element[i], 'web_name']
    pos_id = id_df.loc[id_df.id == picks_df.element[i], 'element_type']
    print(val)
    val_name = str(val).split()[1]
    pri_val = int((str(pri_val).split()[1]))/10
    pos_id = int((str(pos_id).split()[1]))
    pos_name = elements_types_df.loc[elements_types_df.id == pos_id, 'plural_name_short']
    pos_name = str(pos_name).split()[1]

    names.append(val_name)
    price.append(pri_val)
    pos.append(pos_name)

picks_df['Name'] = names
picks_df['Price (£)'] = price
picks_df['Position'] = pos
picks_df = picks_df[['Name', 'Position', 'is_captain', 'is_vice_captain', 'Price (£)']]
print(picks_df)




# functions
