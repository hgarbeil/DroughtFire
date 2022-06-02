import pandas as pd
import numpy as np


class firedata() :
    ### the constructor loads up the current MODIS and VIIRS into a dataframe
    def __init__(self):
        ### get the modis data
        s = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_USA_contiguous_and_Hawaii_7d.csv"

        ### get the viirs data
        s_viirs = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_USA_contiguous_and_Hawaii_7d.csv"
        df = pd.read_csv(s)
        df_viirs = pd.read_csv(s_viirs)
        self.df = df.rename(columns={"bright_t31": "brightness_lwir"})
        self.df['iconfidence']=self.df['confidence']
        self.df.loc[self.df.confidence > 75, 'iconfidence'] = 'high'
        self.df.loc[self.df.confidence<75,'iconfidence']='low'
        self.df_viirs = df_viirs.rename(columns={"confidence":"iconfidence","bright_ti4": "brightness", "bright_ti5": "brightness_lwir"})

        print(df.info())
        self.calc_nti()


    def get_dataframes(self):
        return (self.df, self.df_viirs)

    def calc_nti (self):
        self.df['nti']=(self.df['brightness']-self.df['brightness_lwir'])/(self.df['brightness']+self.df['brightness_lwir'])
        self.df_viirs['nti'] = (self.df_viirs['brightness'] - self.df_viirs['brightness_lwir']) / (self.df_viirs['brightness'] + self.df_viirs['brightness_lwir'])

fdata = firedata()