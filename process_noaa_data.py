from database.db_operations import OceanDatabase
import requests
from bs4 import BeautifulSoup
import pandas as pd

def process_year(year):
    url = f'https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/ascii/ersst.v5.{year}.asc'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html5lib")
    data = soup.find('body').text.split(" ")
    df = pd.DataFrame(data)
    df = pd.to_numeric(df[0])
    df = pd.DataFrame(df.values[df.values != -9999])
    df = df.dropna()
    return df[0].mean()

# Initialize database
db = OceanDatabase(
    dbname="climate_db",
    user="your_username",
    password="your_password"
)

# Create table
db.create_table()

# Process and save data for each year
for year in range(1900, 2001):
    try:
        temperature = process_year(year)
        db.insert_temperature_data(year, temperature)
        print(f"Processed year {year}: {temperature}")
    except Exception as e:
        print(f"Error processing year {year}: {e}") 