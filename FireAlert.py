import pandas as pd 
from urllib.request import urlopen
from collections import namedtuple


class FireAlert:
	# source_url ="https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_USA_contiguous_and_Hawaii_24h.csv"
	source_url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_USA_contiguous_and_Hawaii_24h.csv"
	alerts = []
	AlertVal = namedtuple("AlertVal", ['x', 'y', 'conf'])

	def __init__(self):
		self.df = pd.read_csv(self.source_url)
		self.df['confidence'] = pd.to_numeric(self.df['confidence'])
		self.lat = self.df['latitude']
		self.lon = self.df['longitude']
		self.conf = self.df['confidence']

		myval = self.AlertVal(self.lon[100], self.lat[100], self.conf[100])
		# print (myval)
		self.alerts.append(myval)

		lat = []
		lon = []
		conf = []
		minval = 80.
		#(x, y, z) = self.loadalerts(minval)
		#print(len(x))


	# return array of 3 lists [lon, lat, confidence]
	def loadalerts(self, minval):
		newdf = self.df[self.df['confidence'] > minval]
		newdf_lat = newdf['latitude'].tolist()
		newdf_lon = newdf['longitude'].tolist()
		newdf_conf = newdf['confidence'].tolist()

		print('size of new lat is ' + str(len(newdf_lat)))
		arr = [newdf_lon, newdf_lat, newdf_conf]

		return arr



fa = FireAlert () 




