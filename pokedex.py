import pokebase as pb
import webbrowser
import dash
from dash import html
from dash import dcc
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import requests
import plotly.express as px

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
                html.Hr(),
                html.Div([dcc.Dropdown(id='pokemon-name',options=[{'label':i.capitalize(),'value':i} for i in poke_names_list], value='bulbasaur')],style={'width':'20%', 'margin-left':'auto','margin-right':'auto'}),
                html.Div([html.H1(id='pokemon-name-id')], style={'text-align':'center'}),
                html.Div([
                    html.Div([html.Img(id="pokemon-sprite")],style={'display':'inline-block', 'width':'30%','background-color':'Green', 'margin-right':'10px', 'text-align':'center' }),
                    html.Div([
                        html.Div([html.P(id='pokemon-description'),
                        html.Div([
                            html.Div([html.P(id='pokemon-height')],style={'display':'inline-block'}),
                            html.Div([html.P(id='pokemon-weight')], style={'display':'inline-block'})
                            ])
                            ]),
                            html.P(id='pokemon-ability')], style={'display':'inline-block', 'width':'30%','background-color':'Cyan', 'vertical-align':'top'})
                    ], style={'background-color':'Red'}),
                html.Div([html.P(id='pokemon-type')], style={'background-color':'Orange'}),
                html.Div([html.P(id='pokemon-stat')], style={'background-color':'Pink'}),
                dcc.Graph(id='graph')

])
], style={'background-color':'LightCyan'})

@app.callback(Output('pokemon-name-id','children'),
                [Input('pokemon-name', 'value')],
)
def name_and_id(poke_input):
    poke_request = requests.get("https://pokeapi.co/api/v2/pokemon-species/"+str(poke_input)+"/")
    json_data = poke_request.json()
    name=json_data['name'].capitalize()
    id=str(json_data['id'])
    while len(id)<3:
        id='0'+id
    return "{} #{}".format(name, id)

@app.callback(Output('pokemon-description','children'),
                [Input('pokemon-name', 'value')],
)
def description(poke_input):
    poke_request = requests.get("https://pokeapi.co/api/v2/pokemon-species/"+str(poke_input)+"/")
    json_data = poke_request.json()
    entry=json_data['flavor_text_entries'][0]['flavor_text'].replace('\x0c',' ')
    return "Pokemon's Entry is: {}".format(entry)

@app.callback(Output('pokemon-ability','children'),
                [Input('pokemon-name', 'value')],
)
def ability(poke_input):
    poke_request = requests.get("https://pokeapi.co/api/v2/pokemon/"+str(poke_input)+"/")
    json_data = poke_request.json()
    abilities_json=json_data['abilities']
    abilities = []
    for ability in abilities_json:
        abilities.append(ability['ability']['name'])
    return "Pokemon's Abilities are: {}".format(abilities)

@app.callback(Output('pokemon-type','children'),
                [Input('pokemon-name', 'value')],
)
def types(poke_input):
    poke_request = requests.get("https://pokeapi.co/api/v2/pokemon/"+str(poke_input)+"/")
    json_data = poke_request.json()
    types_json=json_data['types']
    types = []
    for type in types_json:
        types.append(type['type']['name'])
    return "Pokemon's Types are: {}".format(types)

@app.callback(Output('pokemon-height','children'),
                [Input('pokemon-name', 'value')],
)
def height(poke_input):
    poke_request = requests.get("https://pokeapi.co/api/v2/pokemon/"+str(poke_input)+"/")
    json_data = poke_request.json()
    height=json_data['height']/10
    return "Pokemon's Height is: {} m".format(height)

@app.callback(Output('pokemon-weight','children'),
                [Input('pokemon-name', 'value')],
)
def weight(poke_input):
    poke_request = requests.get("https://pokeapi.co/api/v2/pokemon/"+str(poke_input)+"/")
    json_data = poke_request.json()
    weight=json_data['weight']/10
    return html.P("Pokemon's Weight is: {} kg".format(weight))

@app.callback(Output('pokemon-stat','children'),
                [Input('pokemon-name', 'value')],
)
def stats(poke_input):
    poke_request = requests.get("https://pokeapi.co/api/v2/pokemon/"+str(poke_input)+"/")
    json_data = poke_request.json()
    stats_json=json_data['stats']
    stats=[]
    for stat in stats_json:
        stats.append([stat['stat']['name'], stat['base_stat']])
    return "Pokemon's Stats are: {}".format(stats)

@app.callback(Output('pokemon-sprite','src'),Output('pokemon-sprite','style'),
                [Input('pokemon-name', 'value')],
)
def sprite(poke_input):
    poke_request = requests.get("https://pokeapi.co/api/v2/pokemon-species/"+str(poke_input)+"/")
    json_data = poke_request.json()
    id=str(json_data['id'])
    return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"+id+".png", {'width':'200px', 'text-align':'center'}

@app.callback(Output('graph', 'figure'),
                [Input('pokemon-name','value')])

def update_figure(poke_input):
    poke_request = requests.get("https://pokeapi.co/api/v2/pokemon/"+str(poke_input)+"/")
    json_data = poke_request.json()
    stats_json=json_data['stats']
    stats=[]
    for stat in stats_json:
        stats.append([stat['stat']['name'], stat['base_stat']])
    df = pd.DataFrame(stats, columns = ['Stat', 'Base Value'])

    fig = px.bar(df, x="Stat", y="Base Value",
                 )
    return fig
    #
    # traces = []
    # traces.append(go.Scatter(
    # x = df_by_continent["gdpPercap"],
    # y = df_by_continent["lifeExp"],
    # mode='markers',
    # opacity=0.7,
    # marker={'size':15},
    # name=continent_name
    # ))
    #
    # return {'data':traces,
    #         'layout':go.Layout(title='My Plot',
    #                             xaxis={'title': 'GDP Per Cap', 'type':'log'},
    #                             yaxis={'title':'Life Expectancy'})}


if __name__=="__main__":
    app.run_server()
