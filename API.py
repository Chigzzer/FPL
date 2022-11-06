import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
current_gw = 21
url = 'https://fantasy.premierleague.com/api/bootstrap-static/#/'
my_team_url = 'https://fantasy.premierleague.com/api/entry/5768/event/' + \
    str(current_gw) + '/picks/'
my_team = requests.get(my_team_url)
r = requests.get(url)
json = r.json()
json.keys()

print(my_team_url)


elements_df = pd.DataFrame(json['elements'])
elements_types_df = pd.DataFrame(json['element_types'])

teams_df = pd.DataFrame(json['teams'])
print(elements_types_df)
slim_elements_df = elements_df[['second_name', 'team', 'element_type', 'selected_by_percent', 'now_cost', 'minutes',
                                'value_season', 'total_points', 'points_per_game']]

slim_elements_df['position'] = slim_elements_df.element_type.map(elements_types_df.set_index('id').singular_name)
slim_elements_df['team'] = slim_elements_df.team.map(teams_df.set_index('id').name)

slim_elements_df['value'] = slim_elements_df.value_season.astype(float)
slim_elements_df = slim_elements_df.sort_values('value', ascending=False)
print(slim_elements_df)
print('\n')

pivot = slim_elements_df.pivot_table(index='position', values='value', aggfunc=np.mean).reset_index()
pivot = pivot.sort_values('value', ascending=False)
print(pivot)
print('\n')
slim_elements_df = slim_elements_df.loc[slim_elements_df.total_points > 0]
pivot = slim_elements_df.pivot_table(index='position', values='value', aggfunc=np.mean).reset_index()
pivot = pivot.sort_values('value', ascending=False)
print(pivot)
print('\n')
team_pivot = slim_elements_df.pivot_table(index='team', values='value', aggfunc=np.mean).reset_index()
team_pivot = team_pivot.sort_values('value', ascending=False)
print(team_pivot)
print('\n')

fwd_df = slim_elements_df.loc[slim_elements_df.position == 'Forward']
mid_df = slim_elements_df.loc[slim_elements_df.position == 'Midfielder']
def_df = slim_elements_df.loc[slim_elements_df.position == 'Defender']
gk_df = slim_elements_df.loc[slim_elements_df.position == 'Goalkeeper']
print(gk_df)
hist = gk_df.value.hist()
hist.plot()
plt.show()
gk_df = gk_df.sort_values('value', ascending=False).head(10)
print(gk_df)
slim_elements_df.to_csv('C:/Users/chira/Documents/Coding/FPL/fpl_data.csv')


