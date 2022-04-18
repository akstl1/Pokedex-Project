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

poke_names = ['bulbasaur','charmander','charmeleon']

app.layout = html.Div([
    html.Div([
                dcc.Dropdown(id='pokemon_name',options=[{'label':i.capitalize(),'value':i} for i in poke_names], value='bulbasaur'),
    # dcc.Input(id='poke-in',value='1'),
    # html.Button(id='submit-button',n_clicks=0,children='Submit Here', style={'fontSize':24}),
                html.H1(id='poke-out')
])
])

@app.callback(Output('poke-out','children'),
                [Input('pokemon_name', 'value')],
                # [State('poke-in','value')]
)
def output(pokemon_input):
    poke_request = requests.get("https://pokeapi.co/api/v2/pokemon-species/"+pokemon_input+"/")
    json_data = poke_request.json()
    # name=
    # ability=
    # type=
    # height=
    # weight=
    # stat=
    entry=json_data['flavor_text_entries'][0]['flavor_text'].replace('\x0c',' ')
    print(entry)
    hapiness = json_data['base_happiness']
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
