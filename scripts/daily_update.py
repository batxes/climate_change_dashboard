from prefect import flow, task
from src.collectors.noaa_collector import NOAACollector
from src.processors.data_processor import DataProcessor
from src.database.operations import DatabaseManager
from datetime import datetime, timedelta

@task
def collect_data():
    collector = NOAACollector(api_key="YOUR_API_KEY")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    return collector.get_temperature_data(start_date, end_date)

@task
def process_data(df):
    processor = DataProcessor()
    return processor.clean_temperature_data(df)

@task
def save_data(df):
    db = DatabaseManager("connection_string")
    db.save_temperatures(df, source='NOAA')

@flow
def daily_update():
    raw_data = collect_data()
    processed_data = process_data(raw_data)
    save_data(processed_data)

if __name__ == "__main__":
    daily_update() 