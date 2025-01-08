from db_operations import OceanDatabase

db = OceanDatabase(
    dbname="climate_db",
    user="ibai",
    password="ibai"
)

with db.connect() as conn:
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS ocean_temperatures")
