import pokebase as pb
import webbrowser
import dash
from dash import html
from dash import dcc
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import requests

app = dash.Dash()

# get the total count of pokemon from pokeAPI, store as string variable
poke_count=requests.get("https://pokeapi.co/api/v2/pokemon-species")
poke_count_str = str(poke_count.json()['count'])

# request json object with names of all pokemon, using the upper limit of pokemon above
poke_names_json_request = requests.get("https://pokeapi.co/api/v2/pokemon-species/?offset=0&limit="+poke_count_str)
#store request in a variable as json
poke_names_request_response = poke_names_json_request.json()

# create empty list to store pokemon names, loop through request response to populate the list
poke_names_list = []
for name in poke_names_request_response['results']:
    poke_names_list.append(name['name'])

# create app layout

app.layout = html.Div([
    html.Div([
                dcc.Dropdown(id='pokemon-name',options=[{'label':i.capitalize(),'value':i} for i in poke_names_list], value='bulbasaur'),
                html.P(id='pokemon-description')
                # html.P(id='poke-name'),
                # html.P(id='poke-ability'),
                # html.P(id='poke-type'),
                # html.P(id='poke-height'),
                # html.P(id='poke-weight'),
                # html.P(id='poke-stat'),
                # html.P(id='poke-hapiness')
])
])

@app.callback(Output('pokemon-description','children'),
                [Input('pokemon-name', 'value')],
)
def description(poke_input):
    poke_request = requests.get("https://pokeapi.co/api/v2/pokemon-species/"+str(poke_input)+"/")
    json_data = poke_request.json()
    print(json_data['flavor_text_entries'][0]['flavor_text'])
    entry=json_data['flavor_text_entries'][0]['flavor_text'].replace('\x0c',' ')
    return "Pokemon's Entry is: {}".format(entry)


# poke = pb.pokemon(2)
# print('name:', poke)
# print('ability:',poke.abilities[0].ability.name)
# print('move:',poke.moves[0].move.name)
# print('type:',poke.types[0].type)
# print('height:',poke.height)
# print('weight:',poke.weight)
# print('stat:',poke.stats[1].base_stat,poke.stats[1].stat)
# print('entry:',poke.species.flavor_text_entries[0].flavor_text)
# webbrowser.open(poke.sprites.front_default)

#  --------------

# def callback_image(wheel,color):
#     path='../Data/Images/'
#     return encode_image(path+df[(df['wheels']==wheel) & (df['color']==color)]['image'].values[0])
#
if __name__=="__main__":
    app.run_server()
