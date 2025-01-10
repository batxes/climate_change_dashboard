import pandas as pd
import numpy as np

class OceanTempProcessor:
    def __init__(self):
        pass
    
    def process_temperature_data(self, dict):
        for year, value in dict.items():
            dict[year] = value / 100
        return dict
    
    def process_temperature_data_to_df(self, dict):
        df = pd.DataFrame(dict.items(), columns=['year', 'temperature'])
        return df
