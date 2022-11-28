import requests as rq
import pandas as pd

def find_player_code(database, name):
    for i in database['elements']:
        if i['web_name'] == name:
            code = i['code']
    return code

def find_player_id(database, name):
    for i in database['elements']:
        if i['web_name'] == name:
            return i['id']
    return 0


def find_player_name(database, code):
    for i in database['elements']:
        print(code)
        if i['code'] == code:
            name= i['web_name']
    return name


def position(number):
    if number == 1:
        pos = "GK"
    elif number == 2:
        pos = "DEF"
    elif number == 3:
        pos = "MID"
    else:
        pos = "FWD"
    return pos

def find_team(code, database):
    for i in database['teams']:
        if i['id'] ==  code:
            name = i['name']
            return str(name)


# Search functions for each row
def filter_name(df, name):
    df = df.query('name == @name')
    return df

    
def filter_team(df, team):
    df = df.query('team == @team')
    return df

def filter_pos(df, pos):
    df = df.query('position == @pos')
    return df

def reset_df(odf):
    df = odf
    return df

# Add fucntions to add columns/renamr column to table.
def add_column(name, df, main_df):
    df[name] = main_df[name] 
    return df

def remove_column(name, df):
    df = df.drop(name, axis = 1) 
    return df

def sort_db(name, db):
    db = db.sort_values(by=['name'], ascending=False)
    return db

# Obtain points
def player_weekPoints(player_id):
   
    points_api = 'https://fantasy.premierleague.com/api/element-summary/' + str(player_id) + '/'
    points_data = rq.get(points_api)
    points_db = points_data.json()
    points_df = pd.DataFrame(points_db['history'])
    points_df_points = points_df['total_points'] #gets player id
    player_gw_points=[]
    player_total_points = []
    for point in points_df_points:
        player_gw_points.append(point)
    for i in range(len(player_gw_points)):
        if i == 0:
            player_total_points.append(player_gw_points[i])
        else:
            player_total_points.append(player_gw_points[i] + player_total_points[i-1])

    return player_gw_points, player_total_points


def get_player_list(db):
    player_list = []
    teams = []
    for player in db['elements']:
        team = find_team(player['team'], db)
        if team not in teams:
            teams.append(team)
        pl = [player['web_name'], team]
        player_list.append(pl)
    return player_list, teams