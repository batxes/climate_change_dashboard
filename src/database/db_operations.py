from sqlalchemy import create_engine, text
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st

class OceanDatabase:
    def __init__(self, type="local"):
        # If individual parameters are provided, use them
        if type == "local":
            dbname=st.secrets["postgres_local"]["dbname"],
            user=st.secrets["postgres_local"]["user"],
            password=st.secrets["postgres_local"]["password"],
            host=st.secrets["postgres_local"]["host"],
            port=st.secrets["postgres_local"]["port"]
            connection_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        elif type == "prod":
            # Otherwise, use environment variable
            connection_url = st.secrets["postgres_prod"]["DATABASE_URL"]
            
        self.engine = create_engine(connection_url)

    def create_table(self):
        with self.engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ocean_temperatures (
                    year INTEGER NOT NULL UNIQUE,
                    temperature DECIMAL(6,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_ocean_temps_year 
                ON ocean_temperatures(year);
            """))
            conn.commit()

    def insert_temperature_data(self, data_dict):
        """
        Insert temperature data from a dictionary
        
        Parameters:
        data_dict (dict): Dictionary with years as keys and temperatures as values
        """
        try:
            with self.engine.connect() as conn:
                # Convert dictionary to list of dictionaries with native Python types
                records = [
                    {
                        "year": int(year),  # Convert numpy.int64 to int
                        "temperature": float(temp)  # Convert numpy.float64 to float
                    } 
                    for year, temp in data_dict.items()
                ]
                
                # Batch insert/update
                conn.execute(
                    text("""
                        INSERT INTO ocean_temperatures (year, temperature)
                        VALUES (:year, :temperature)
                        ON CONFLICT (year) DO UPDATE 
                        SET temperature = EXCLUDED.temperature,
                            updated_at = CURRENT_TIMESTAMP
                    """),
                    records
                )
                conn.commit()
                print(f"Successfully inserted/updated {len(records)} records")
                
        except SQLAlchemyError as e:
            print(f"Error inserting data: {str(e)}")
            raise

    def get_data(self, start_year=None, end_year=None):
        query = "SELECT * FROM ocean_temperatures"
        if start_year and end_year:
            query += f" WHERE year BETWEEN {start_year} AND {end_year}"
        query += " ORDER BY year"
        
        return pd.read_sql(query, self.engine) 

    def table_exists(self):
        """
        Check if the ocean_temperatures table exists and contains data
        Returns: bool
        """
        with self.engine.connect() as conn:
            # Check if table exists
            table_exists_query = text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'ocean_temperatures'
                );
            """)
            table_exists = conn.execute(table_exists_query).scalar()
            
            if not table_exists:
                return False
            
            # Check if table has data
            data_exists_query = text("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM ocean_temperatures 
                    WHERE year IS NOT NULL 
                    AND temperature IS NOT NULL 
                    LIMIT 1
                );
            """)
            has_data = conn.execute(data_exists_query).scalar()
            print ("has_data", has_data)
            
            return has_data

    def drop_table(self):
        """Drop the ocean_temperatures table if it exists"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("DROP TABLE IF EXISTS ocean_temperatures"))
                conn.commit()
                print("Table dropped successfully")
        except SQLAlchemyError as e:
            print(f"Error dropping table: {str(e)}")
