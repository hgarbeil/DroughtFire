from urllib.request import urlopen
import json
import pandas as pd

import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import dash
from dash import html
from dash.dependencies import Input,Output,State
from firedata import *
from droughts import *


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

app = dash.Dash() 


statecaps = pd.read_csv("/Users/hg1/data/us-state-capitals.csv")
statecaps.info()

fdata = firedata()
mydroughts = droughts()
df,df_viirs = fdata.get_dataframes()

print (df_viirs.info())
#df = pd.read_csv("")
#df['geoid'] = df['geoid'].str[4:]
lat=df['latitude']

nmind = statecaps[statecaps['State']=="New Mexico"]
nm_lat = nmind.at[30,'Lat']
nm_lon = nmind.at[30,'Lon']

df_new = pd.concat([df,df_viirs],axis=0)
print(df_new.info())

fig = px.scatter_mapbox(df_new, lat='latitude',lon='longitude', color='brightness',zoom=4,
						center=dict(lat=nm_lat,lon=nm_lon),height=800,
						hover_data=['latitude','longitude','confidence', 'nti','brightness_lwir'])

fig.update_layout(mapbox_style="open-street-map")
#fig.show()
app.layout = html.Div([ 
	html.Div (style={'width': "100%", "text-align": "center"},
        children=[
            html.Label('Recent Fires (Last 24 Hours)')
        ]),
	html.Div(
	style={'width':"85%",'display':'inline-block'},
	children=[
	dash.dcc.Dropdown(
		id='dd_locale',
		#options=[{'label':"New Mexico", 'value':'New Mexico'}],
		options=[{'label':i['State'],'value':i['State']} for j,i in statecaps.iterrows()],
		value='New Mexico'),
	html.Div([
		dash.dcc.Graph(id='my_map', figure=fig)
	])
    ])
])

@app.callback (
	[Output(component_id='my_map', component_property='figure')],
	[Input(component_id='dd_locale', component_property='value')]
)

def update_map(stateval) :
	nmind = statecaps[statecaps['State']==stateval].reset_index()
	nm_lat = nmind.at[0,'Lat']
	nm_lon = nmind.at[0,'Lon']

	df_new['b10'] = df_new['brightness']*10.
	fig = px.choropleth_mapbox(mydroughts.df_droughts, geojson=counties, locations='FIPSNew',
					   color='DSCI', color_continuous_scale="Viridis",
					   center={"lat": nm_lat, "lon": nm_lon}, zoom=5, hover_name='County',
					   hover_data=['ValidEnd', 'D4', 'D4'])
	fig.update_layout(mapbox_style="white-bg",
					  mapbox_zoom=5)
	fig2=px.scatter_mapbox(df_new,
			lat='latitude',
			lon='longitude',
			color='b10',
			#color_discrete_sequence='agsunset',
			color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
			hover_data=['confidence','brightness']
	)
	fig.add_trace(fig2.data[0])




	return ([fig])
		

app.run_server(debug=True, use_reloader=False) 
