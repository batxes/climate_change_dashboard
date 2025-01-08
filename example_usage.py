import numpy as np
from src.database.db_operations import OceanDatabase

# Initialize database
db = OceanDatabase(
    dbname="climate_db",
    user="ibai",
    password="ibai"
)

# Create table
db.create_table()

# Insert temperature data for 1900-2000
for year in range(1900, 2001):
    # Replace this with your actual temperature data
    temperature = np.random.uniform(15, 20)  # Example random data
    db.insert_temperature_data(year, temperature)

# Later, add measurements for specific years
db.update_measurements(1950, lower_confidence_interval=18.5, upper_confidence_interval=19.0)
db.update_measurements(1951, lower_confidence_interval=18.7, upper_confidence_interval=19.2)
db.update_measurements(1900, lower_confidence_interval=18.7, upper_confidence_interval=19.2)

# Retrieve data
df = db.get_data(start_year=1900, end_year=2000)
print(df) 