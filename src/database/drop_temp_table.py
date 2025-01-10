from db_operations import OceanDatabase


db = OceanDatabase(type="prod")

db.drop_table()
