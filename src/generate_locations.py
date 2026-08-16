import os
from dotenv import load_dotenv
import mysql.connector
import math
import random

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

cursor.execute( "SELECT a1.address, a1.long_name, a2.long_name as storage, sc.racks, sc.columns_count, sc.shelves FROM Areas a1 " \
                "LEFT JOIN Storage_configuration sc ON a1.zone_address = sc.area_address " \
                "LEFT JOIN Areas a2 ON a1.zone_address = a2.address WHERE a1.zone_address IS NOT NULL;")
locations_data = cursor.fetchall()


cursor.execute( "SELECT a.long_name, sc.racks, sc.shelves FROM Storage_configuration sc " \
                "LEFT JOIN Areas a ON sc.area_address = a.address;")
store_configurations_data = cursor.fetchall()



store_configurations = []

box_storages = ["DPL", "KLT", "WHN", "ASM", "LOG", "DCN", "SP1"]
pallet_storages = ["MTR", "RPK", "SBC", "VNX", "WHS", "WHE", "PRT", "PKG", "BUF", "SUP", "DCS", "DCR", "SP2", "SP3"]
packing_boxes = ["C1", "C2", "C3"]
packing_pallets_E = ["11D", "12D", "13D", "14D", "15D", "16D"]
packing_pallets_H = ["21D", "22D", "23D"]
packing_pallets = packing_pallets_E + packing_pallets_H
pallet_height_limit_E = 3

for store_configuration in store_configurations_data:
    if store_configuration[0] in box_storages:
        for rack in range(1, store_configuration[1]+1):
            for shelf in range(1 ,store_configuration[2]+1):
                packing_type = random.choice(packing_boxes)
                store_configurations.append((store_configuration[0], rack, shelf, packing_type))

    if store_configuration[0] in pallet_storages:
        for rack in range(1, store_configuration[1]+1):
            for shelf in range(1 ,store_configuration[2]+1):
                
                if shelf == 1:
                    packing_type = random.choice(packing_pallets)
                    store_configurations.append((store_configuration[0], rack, shelf, packing_type))
                elif packing_type in packing_pallets_E:
                    if shelf > pallet_height_limit_E:
                        packing_type = random.choice(packing_pallets_E[:3])
                        store_configurations.append((store_configuration[0], rack, shelf, packing_type))
                    else:
                        packing_type = random.choice(packing_pallets_E)
                        store_configurations.append((store_configuration[0], rack, shelf, packing_type))
                elif packing_type in packing_pallets_H:
                    packing_type = random.choice(packing_pallets_H)
                    store_configurations.append((store_configuration[0], rack, shelf, packing_type))

locations = []

category_1 = 0.3
category_2 = 0.5

if category_1 + category_2 > 1:
    print("Error: You cannot use combination extending 100%")
    exit()
elif category_1 < 0 or category_2 < 0:
    print("Error: Category percentages cannot be negative")
    exit()

location_statuses = ["O", "F"]

for location in locations_data:
    
    current_shelf = int(location[1][-2:])
    current_rack = int(location[1][3:5])
    current_store = location[2]
    current_category_1 = math.ceil(location[5]*category_1)
    current_category_2 = math.floor(location[5]*category_2)

    packing_type = None
    for store_configuration in store_configurations:
        if (store_configuration[0] == current_store and store_configuration[1] == current_rack and store_configuration[2] == current_shelf):
            packing_type = store_configuration[3]
            break

    if packing_type is None:
        print("Error: Couldn't find packing_type in storage_configurations")
        exit()

    location_status = random.choices(location_statuses, weights = [85,15], k = 1)[0]

    if current_shelf <= current_category_1:
        locations.append((location[0], packing_type, f"{location[2][0]}1", location_status))
    elif current_shelf <= (current_category_1 + current_category_2):
        locations.append((location[0], packing_type, f"{location[2][0]}2", location_status))
    else:
        locations.append((location[0], packing_type, f"{location[2][0]}3", location_status))


if not locations:
    print("No locations generated. Nothing to insert.")
    exit()

print(f"Preparing to insert {len(locations)} locations.")

cursor.executemany( "INSERT INTO Locations (address, packing_type, location_category, location_status) " \
                "VALUES (%s, %s, %s, %s)",
                locations)


connection.commit()
print(f"Inserted {cursor.rowcount} rows.")


cursor.close()
connection.close()
