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

#df = pd.read_csv("")
#df['geoid'] = df['geoid'].str[4:]
lat=df['latitude']

nmind = statecaps[statecaps['State']=="New Mexico"]
nm_lat = nmind.at[30,'Lat']
nm_lon = nmind.at[30,'Lon']

df_new = pd.concat([df,df_viirs],axis=0)

fig = px.scatter_mapbox(df_new, lat='latitude',lon='longitude', color='brightness',zoom=4,
						center=dict(lat=nm_lat,lon=nm_lon),height=800,
						hover_data=['latitude','longitude','iconfidence', 'nti','brightness_lwir'])

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
	html.Pre(""),
	dash.dcc.Checklist(id='layer-checklist',options=['Droughts','VIIRS Fires','MODIS Fires','US Capitals'],
		value=['Droughts', 'VIIRS Fires', 'MODIS Fires'],style={'display':'inline-block','width':'35%'}),
	html.Button ("SUBMIT", id='update-button',n_clicks=0,style={'display':'inline-block','width':'20%'}),
	html.Pre(""),
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
	[Input(component_id='dd_locale', component_property='value')],
	[Input(component_id='update-button', component_property='n_clicks')],
	[State(component_id='layer-checklist',component_property='value')]
)

def update_map(stateval,n_clicks, checkvals) :
	fdata = firedata()
	mydroughts = droughts()
	df, df_viirs = fdata.get_dataframes()

	nmind = statecaps[statecaps['State']==stateval].reset_index()
	nm_lat = nmind.at[0,'Lat']
	nm_lon = nmind.at[0,'Lon']

	# make empy data frame if neither viirs or modis is checked
	if ('MODIS Fires' not in checkvals and 'VIIRS Fires' not in checkvals):
		df_new = pd.DataFrame(columns=['latitude', 'longitude', 'iconfidence', 'nti', 'brightness_lwir','colors'])
	else :
		if ('MODIS Fires' in checkvals and 'VIIRS Fires' in checkvals) :
			df_new = pd.concat([df, df_viirs])
		if ('MODIS Fires' in checkvals and 'VIIRS Fires' not in checkvals) :
			df_new = df.copy()
		if ('VIIRS Fires' in checkvals and 'MODIS Fires' not in checkvals):
			df_new = df_viirs.copy()



	df_new.drop(df_new.index[df_new['iconfidence']!='high'],inplace=True)
	df_new.loc[df_new.brightness>15000,'brightness']=15000
	df_new['b10']=df_new['brightness']*5.
	df_new['size']=.1
	df_new['colors']='rgb(255,255,200)'
	if 'Droughts' in checkvals :
		fig = px.choropleth_mapbox(mydroughts.df_droughts, geojson=counties, locations='FIPSNew',
					   color='PctArea', color_continuous_scale="Viridis",
					   range_color=[0,100],
					   center={"lat": nm_lat, "lon": nm_lon}, zoom=5, hover_name='County',
					   hover_data=['ValidEnd', 'D4', 'D4'])

		fig.update_layout(mapbox_style="white-bg",
					  mapbox_zoom=5)

		fig2=px.scatter_mapbox(df_new,
			lat='latitude',
			lon='longitude',
			color='colors',
			size='size',
			size_max=5,
			#color_discrete_sequence='agsunset',
			#color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
			hover_data=['iconfidence','brightness']
		)
		fig.add_trace(fig2.data[0])

	else :
		fig = px.scatter_mapbox(df_new, lat='latitude', lon='longitude', color='brightness', zoom=4,
								center=dict(lat=nm_lat, lon=nm_lon), height=800,
								hover_data=['latitude', 'longitude', 'iconfidence', 'nti', 'brightness_lwir'])
		fig.update_layout(mapbox_style="open-street-map")

	# fig2.add_trace(px.scatter_mapbox(df_new, lat='latitude',
	# 		lon='longitude',
	# 		mode='markers',
	# 		color='rgb(255,255,255',
	# 		size=12))


	return ([fig])
		

app.run_server(debug=True, use_reloader=False) 
