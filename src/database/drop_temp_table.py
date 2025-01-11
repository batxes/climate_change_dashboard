from db_operations import ClimateDatabase


db = ClimateDatabase(type="local")

db.drop_global_temperature_table()
#db.drop_ocean_temperature_table()