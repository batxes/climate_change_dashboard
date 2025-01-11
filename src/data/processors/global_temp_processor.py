import pandas as pd
import numpy as np

class GlobalTempProcessor:
    def __init__(self):
        pass
    
    def process_temperature_data(self, dict):
        for year, value in dict.items():
            dict[year] = value / 100
        return dict
    
    def calculate_pre_industrial_average_temperature(self, df):
        pre_industrial_average_temperature = 0
        pre_industrial_years = 0
        for index, row in df.iterrows():
            if row['year'] >= 1850 and row['year'] <= 1900:
                pre_industrial_average_temperature += row['temperature'] 
                pre_industrial_years += 1
        pre_industrial_average_temperature /= pre_industrial_years
        return pre_industrial_average_temperature
    
    def process_temperature_data_to_df(self, dict):
        df = pd.DataFrame(dict.items(), columns=['year', 'temperature'])
        return df
