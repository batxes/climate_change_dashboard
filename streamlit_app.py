import streamlit as st
import plotly.express as px
from src.database.db_operations import OceanDatabase
from src.collectors.ocean_temp_collector import OceanTempCollector
from src.data.processors.ocean_temp_processor import OceanTempProcessor
from datetime import date

def main():
    st.title("Climate Data Dashboard")

    db = OceanDatabase(type="local")

    # Date range selector
    start_year = 1854
    end_year = 2024

    # Check if table exists and handle data accordingly
    if not db.table_exists():

        st.info("Initializing database...")
        db.create_table()
        
        # Create a placeholder for the progress message
        progress_message = st.empty()
        
        with st.spinner(f'Collecting initial data...'):
            years_to_collect = range(start_year, end_year)
            progress_message.text(f"Collecting data for years {years_to_collect}")

            ocean_temp_collector = OceanTempCollector()
            ocean_temp_processor = OceanTempProcessor()
            
            new_data = ocean_temp_collector.get_year_mean(start_year, end_year)
            new_data = ocean_temp_processor.process_temperature_data(new_data)
            db.insert_temperature_data(new_data)
            
            progress_message.empty()
            st.success(f'Database initialized with {len(years_to_collect)+1} years of data')
    
    # Get data for visualization
    data = db.get_data(start_year, end_year)

    # Create visualizations
    fig = px.line(data, x='year', y='temperature',
                  title='Temperature Trends')
    st.plotly_chart(fig)


if __name__ == "__main__":
    main() 