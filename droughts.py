
from urllib.request import urlopen
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express  as px
import geopandas as gpd
import json


### get drought monitor current data from web
# process the fips data so it can be used with the geojson info
class droughts():
    def __init__(self):
        self.df_droughts = pd.read_csv('https://droughtmonitor.unl.edu/DmData/GISData.aspx?mode=table&aoi=county&date=')
        newfips=self.df_droughts['FIPS'].copy()
        self.df_droughts['FIPSNew'] = newfips.map("{:05}".format)
        self.calc_DSCI()

    ###
    # https://droughtmonitor.unl.edu/About/AbouttheData/DSCI.aspx
    def calc_DSCI (self) :
        self.df_droughts['DSCI']=self.df_droughts['D0']+2*self.df_droughts['D1']+3*self.df_droughts['D2'] + 4*self.df_droughts['D3'] + 5*self.df_droughts['D4']
        #self.df_droughts['DSCI'].index(self.df_droughts[self.df_droughts['DSCI']]=15000
        self.df_droughts.loc[self.df_droughts.DSCI > 15000, 'DSCI'] = 15000






