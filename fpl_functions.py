
def find_player_code(database, name):
    for i in database['elements']:
        if i['web_name'] == name:
            code = i['code']
    return code


def find_player_name(database, code):
    for i in database['elements']:
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