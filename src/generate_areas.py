import os
from dotenv import load_dotenv
import mysql.connector


load_dotenv()

try:
    connection = mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )

    print("Connected successfully!")

except mysql.connector.Error as error:
    print(f"Database connection failed: {error}")
    exit()

cursor = connection.cursor()


cursor.execute("SELECT MAX(address) FROM Areas;")
max_address = cursor.fetchone()

if max_address[0] is None:
    print("Areas table is empty.")
    exit()

next_address = max_address[0] + 1


cursor.execute( "SELECT sc.area_address, sc.racks, sc.columns_count, sc.shelves, a.long_name, a.building_address FROM Storage_configuration as sc " \
                "LEFT JOIN Areas as a ON sc.area_address = a.address")
storage_configurations = cursor.fetchall()


rows = []

for storage in storage_configurations:
    storage_address = storage[0]
    storage_racks = storage[1]
    storage_columns = storage[2]
    storage_shelves = storage[3]
    storage_name = storage[4]
    building_address = storage[5]


    for rack in range(1, storage_racks+1):
        for column in range(1, storage_columns+1):
            for shelf in range(1, storage_shelves+1):
                rows.append((next_address, f"{storage_name}{rack:02d}{column:02d}{shelf:02d}", storage_address, building_address))
                next_address += 1


cursor.executemany( "INSERT INTO Areas (address, long_name, zone_address, building_address) " \
                "VALUES (%s, %s, %s, %s)",
                rows)

connection.commit()
print(f"Inserted {cursor.rowcount} rows.")


cursor.close()
connection.close()

