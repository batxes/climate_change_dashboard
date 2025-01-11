import pandas as pd

class GlobalTempCollector:

    def __init__ (self):
        pass

    def get_year_mean(self, year_from, year_to):
        try:
            df = pd.read_csv('https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.txt', skiprows=7, sep='\s+')
        except Exception as e:
            print(f"Error collecting global temperature data: {e}")
            return []
        try:
            df = df.iloc[:, :-1]
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.dropna(subset=["Year"])
            df["Year"] = df["Year"].astype(int)
            df["J-D"] = df["J-D"].astype(int)
            df = df.query(f'Year >= {year_from} and Year <= {year_to}')
            years = df['Year'].values.tolist()
            means = df['J-D'].values.tolist()
            return dict(zip(years, means))
        except Exception as e:
            print(f"Error processing global temperature data: {e}")
            return []

