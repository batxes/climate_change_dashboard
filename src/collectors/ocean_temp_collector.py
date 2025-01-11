import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

class OceanTempCollector:
    def __init__(self):
        pass

    def get_year_mean(self, year_from, year_to):
        ocean_temp_dict = {}
        for year in np.arange(year_from, year_to+1, 1):
            try:
                url = f'https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/ascii/ersst.v5.{year}.asc'
                res = requests.get(url)
                soup = BeautifulSoup(res.content, "html5lib")
                data = soup.find('body').text.split(" ")
                df = pd.DataFrame(data)
                df = pd.to_numeric(df[0])
                df = pd.DataFrame(df.values[df.values != -9999]) # -9999 is the missing value code
                df = df.dropna()
                ocean_temp_dict[year] = df[0].mean()
                print("year", year, "mean", ocean_temp_dict[year])
            except Exception as e:
                print(f"Error processing year {year}: {e}")
        return ocean_temp_dict
    
