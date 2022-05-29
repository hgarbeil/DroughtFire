import pandas as pd
import numpy as np


class firedata() :
    ### the constructor loads up the current MODIS and VIIRS into a dataframe
    def __init__(self):
        ### get the modis data
        s = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_USA_contiguous_and_Hawaii_24h.csv"

        ### get the viirs data
        s_viirs = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_USA_contiguous_and_Hawaii_24h.csv"
        df = pd.read_csv(s)
        df_viirs = pd.read_csv(s_viirs)
        self.df = df.rename(columns={"bright_t31": "brightness_lwir"})
        self.df_viirs = df_viirs.rename(columns={"bright_ti4": "brightness", "bright_ti5": "brightness_lwir"})
        print(df.info())
        self.calc_nti()

        ### current drought map
        dd= pd.read_csv('https://droughtmonitor.unl.edu/DmData/GISData.aspx?mode=table&aoi=county&date=')
        dd.info()

    def get_dataframes(self):
        return (self.df, self.df_viirs)

    def calc_nti (self):
        self.df['nti']=(self.df['brightness']-self.df['brightness_lwir'])/(self.df['brightness']+self.df['brightness_lwir'])
        self.df_viirs['nti'] = (self.df_viirs['brightness'] - self.df_viirs['brightness_lwir']) / (self.df_viirs['brightness'] + self.df_viirs['brightness_lwir'])

fdata = firedata()