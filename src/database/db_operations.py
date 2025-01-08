from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime

class OceanDatabase:
    def __init__(self, dbname="climate_db", user="your_username", password="your_password", host="localhost", port="5432"):
        # Create SQLAlchemy engine
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')

    def create_table(self):
        with self.engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ocean_temperatures (
                    id SERIAL PRIMARY KEY,
                    year INTEGER NOT NULL UNIQUE,
                    temperature DECIMAL(6,2),
                    lower_confidence_interval DECIMAL(6,2),
                    upper_confidence_interval DECIMAL(6,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_ocean_temps_year 
                ON ocean_temperatures(year);
            """))
            conn.commit()

    def insert_temperature_data(self, year, temperature):
        with self.engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO ocean_temperatures (year, temperature)
                    VALUES (:year, :temperature)
                    ON CONFLICT (year) DO UPDATE 
                    SET temperature = EXCLUDED.temperature,
                        updated_at = CURRENT_TIMESTAMP
                """),
                {"year": year, "temperature": temperature}
            )
            conn.commit()

    def update_measurements(self, year, lower_confidence_interval=None, upper_confidence_interval=None):
        with self.engine.connect() as conn:
            updates = []
            params = {"year": year}
            
            if lower_confidence_interval is not None:
                updates.append("lower_confidence_interval = :lower_confidence_interval")
                params["lower_confidence_interval"] = lower_confidence_interval
            if upper_confidence_interval is not None:
                updates.append("upper_confidence_interval = :upper_confidence_interval")
                params["upper_confidence_interval"] = upper_confidence_interval
            
            if updates:
                updates.append("updated_at = CURRENT_TIMESTAMP")
                query = f"""
                    UPDATE ocean_temperatures 
                    SET {', '.join(updates)}
                    WHERE year = :year
                """
                conn.execute(text(query), params)
                conn.commit()

    def get_data(self, start_year=None, end_year=None):
        query = "SELECT * FROM ocean_temperatures"
        if start_year and end_year:
            query += f" WHERE year BETWEEN {start_year} AND {end_year}"
        query += " ORDER BY year"
        
        return pd.read_sql(query, self.engine) 