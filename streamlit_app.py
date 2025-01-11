import streamlit as st
import plotly.express as px
from src.database.db_operations import ClimateDatabase
from src.collectors.ocean_temp_collector import OceanTempCollector
from src.collectors.global_temp_collector import GlobalTempCollector
from src.data.processors.ocean_temp_processor import OceanTempProcessor
from src.data.processors.global_temp_processor import GlobalTempProcessor
from datetime import date

ocean_temp_start_year = 1854
ocean_temp_end_year = 2024
global_temp_start_year = 1880
global_temp_end_year = 2024

def main():
    st.title("Climate Data Dashboard")

    db = ClimateDatabase(type="prod")

    if not db.ocean_temperature_table_exists():
        st.info("Initializing ocean temperature database...")
        db.create_ocean_temperature_table()
        with st.spinner(f'Collecting initial data...'):
            ocean_temp_collector = OceanTempCollector()
            ocean_temp_processor = OceanTempProcessor()
            new_data = ocean_temp_collector.get_year_mean(ocean_temp_start_year, ocean_temp_end_year)
            new_data = ocean_temp_processor.process_temperature_data(new_data)
            db.insert_ocean_temperature_data(new_data)
            st.success(f'Ocean temperature database initialized')

    if not db.global_temperature_table_exists():
        st.info("Initializing global temperature database...")
        db.create_global_temperature_table()
        with st.spinner(f'Collecting initial data...'):
            global_temp_collector = GlobalTempCollector()
            global_temp_processor = GlobalTempProcessor()
            new_data = global_temp_collector.get_year_mean(global_temp_start_year, global_temp_end_year)
            new_data = global_temp_processor.process_temperature_data(new_data)
            db.insert_global_temperature_data(new_data)
            st.success(f'Global temperature database initialized')
    
    # Get data for visualization
    ocean_temp_data = db.get_ocean_temperature_data(ocean_temp_start_year, ocean_temp_end_year)
    global_temp_data = db.get_global_temperature_data(global_temp_start_year, global_temp_end_year)
    # pre-industrial average temperature is stablished to be 0
    #global_temp_processor = GlobalTempProcessor()
    #pre_industrial_average_temperature = global_temp_processor.calculate_pre_industrial_average_temperature(global_temp_data)

    pre_industrial_average_temperature = 0
    # Create visualizations
    fig = px.line(ocean_temp_data, x='year', y='temperature',
                  title='Ocean Temperature Trends')
    st.plotly_chart(fig)

    fig = px.line(global_temp_data, x='year', y='temperature',
                  title='Global Temperature Trends')
    fig.add_hline(y=pre_industrial_average_temperature, line_dash="dash", line_color="grey", annotation_text="Pre-Industrial Average (1850-1900)")
    fig.add_hline(y=1.5, line_dash="dash", line_color="red", annotation_text="1.5°C (2015 Paris Agreement)")
    st.plotly_chart(fig)


if __name__ == "__main__":
    main() 