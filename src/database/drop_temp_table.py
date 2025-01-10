from db_operations import OceanDatabase

db = OceanDatabase(
    dbname="climate_db",
    user="ibai",
    password="ibai"
)

db.drop_table()
